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
    try:
        key = f"post-{slug_value}"

        if value := cache.get(key):
            instance = orjson.loads(value)
        else:
            query = Post.objects.published().get(slug=slug_value)
            instance = PostSerializer(query).data

            set_cache(key, orjson.dumps(instance))
        return Response(instance)
    except Exception:
        return Response(status=status.HTTP_404_NOT_FOUND)


class PostListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Post.objects.published()
    serializer_class = PostOverviewSerializer

    @action(detail=False, methods=[HM.GET])
    def overview(self, req: Request):
        """
        Custom action to retrieve an overview of posts, and cache content.

        Response: A serialized representation of the first four posts
        from the queryset, formatted as a JSON response.
        """
        key = "post-overview"
        if (value := cache.get(key)):
            data = orjson.loads(value)
        else:
            data = self.serializer_class(self.queryset[:4], many=True).data
            set_cache(key, orjson.dumps(data))
        return Response(data)

    def list(self, req: Request, *args, **kwargs):
        page = req.query_params.get("page", 1)
        key = f"post-list-page-{page}"

        if (value := cache.get(key)):
            return Response(orjson.loads(value))
        else:
            resp = super().list(req, *args, **kwargs)
            set_cache(key, orjson.dumps(resp.data))
            return resp


class PostManagerViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = PostManagerSerializer
    lookup_field = "slug"
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)