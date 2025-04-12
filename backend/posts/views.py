from http import HTTPMethod as HM

from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Post
from .serializers import (
    PostSerializer,
    PostOverviewSerializer,
)


class PostViewSet(
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """ this section not complete, because there is not auth system. """
    queryset = Post.objects.published()
    serializer_class = PostSerializer
    lookup_field = "slug"


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
