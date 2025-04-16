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
        Custom action to retrieve an overview of posts.

        Response: A serialized representation of the first four posts
        from the queryset, formatted as a JSON response.
        """
        return Response(
            self.serializer_class(self.queryset[:4], many=True).data
        )


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