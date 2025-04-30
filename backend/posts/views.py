from http import HTTPMethod as HM

import orjson
from django.core.cache import cache
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import api_view, action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Post
from .serializers import (
    PostSerializer,
    PostManagerSerializer,
    PostOverviewSerializer,
)
from backend.celery import set_cache
from user_panel.auth import JWTAuthentication


@api_view([HM.GET])
def get_post(req: Request, slug_value):
    """
    Retrieve a post based on the provided slug value.

    This function checks if the post data is cached. If cached data is found, it is deserialized using `orjson`.
    If the post data is not cached, it queries the database for the post object, serializes it using `PostSerializer`,
    and caches the serialized data.

    Parameters:
        req (Request): The HTTP request object.
        slug_value (str): The unique slug identifier of the post.

    Returns:
        Response: A JSON response containing the post data.
                  If the post is not found, it returns a 404 Not Found status.
    """
    try:
        key = f"post-{slug_value}"

        if value := cache.get(key):
            instance = orjson.loads(value)
        else:
            query = Post.objects.published().get(slug=slug_value)
            instance = PostSerializer(query).data

            set_cache.delay(key, orjson.dumps(instance))
        return Response(instance)
    except Exception:
        return Response(status=status.HTTP_404_NOT_FOUND)


class PostListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    A viewset for handling post-related operations with caching.

    This viewset provides two main functionalities:
      - `overview`: Retrieves an overview of the top 4 posts, with caching implemented.
      - `list`: Handles paginated post retrieval, with caching for each page.

    Attributes:
        queryset (QuerySet): A QuerySet of published posts.
        serializer_class (Serializer): The serializer used for serializing post data.
    """
    queryset = Post.objects.published()
    serializer_class = PostOverviewSerializer

    @action(detail=False, methods=[HM.GET])
    def overview(self, req: Request):
        """
        Retrieves an overview of the top 4 posts.

        This method checks if the overview data is cached. If cached data exists, it is deserialized using `orjson`.
        Otherwise, it fetches the top 4 posts from the queryset, serializes them, and caches the result.

        Parameters:
            req (Request): The HTTP request object.

        Returns:
            Response: A JSON response containing an overview of the top 4 posts.
        """
        key = "post-overview"
        if (value := cache.get(key)):
            data = orjson.loads(value)
        else:
            data = self.serializer_class(self.queryset[:4], many=True).data
            set_cache.delay(key, orjson.dumps(data))
        return Response(data)

    def list(self, req: Request, *args, **kwargs):
        """
        Retrieves a paginated list of posts.

        This method retrieves the requested page number from query parameters, constructs a cache key, and checks
        if the page data is cached. If cached data exists, it is deserialized using `orjson`.
        Otherwise, it calls the default list method to fetch paginated posts, caches the result, and returns the response.

        Parameters:
            req (Request): The HTTP request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: A JSON response containing the paginated list of posts.
        """
        page = req.query_params.get("page", 1)
        key = f"post-list-page-{page}"

        if (value := cache.get(key)):
            return Response(orjson.loads(value))
        else:
            resp = super().list(req, *args, **kwargs)
            set_cache.delay(key, orjson.dumps(resp.data))
            return resp


class PostManagerViewSet(
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    A viewset for managing posts owned by the authenticated user.

    This viewset provides CRUD (Create, Read, Update, Delete) operations for posts,
    ensuring that only the posts belonging to the authenticated user can be accessed
    or modified. Authentication and permissions are enforced using JWT and `IsAuthenticated`.

    Attributes:
        serializer_class (Serializer): Specifies the serializer used for post data.
        lookup_field (str): Specifies that posts are identified by their unique slug.
        authentication_classes (list): Ensures requests are authenticated using JWT.
        permission_classes (list): Ensures only authenticated users have access.
    """
    serializer_class = PostManagerSerializer
    list_serializer_class = PostOverviewSerializer
    lookup_field = "slug"
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Retrieves the queryset of posts owned by the authenticated user.

        This method filters the posts in the database to only include those
        that belong to the current user making the request.

        Returns:
            QuerySet: A QuerySet of posts owned by the authenticated user.
        """
        return Post.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Handles the creation of a new post and used by create mixin.

        This method ensures that the user field is automatically set to
        the current authenticated user when a post is created.

        Parameters:
            serializer (Serializer): The serializer containing the validated post data.

        Returns:
            None
        """
        serializer.save(user=self.request.user)

    def list(self, req: Request):
        queryset = self.get_queryset()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.list_serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.list_serializer_class(queryset, many=True)
        return Response(serializer.data)