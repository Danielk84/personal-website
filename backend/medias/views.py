from django.views.static import serve
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Photo
from .serializers import PhotoSerializer
from user_panel.auth import JWTAuthentication
from posts.models import Post


class PhotoManagerViewSet(viewsets.ViewSet):
    serializer_class = PhotoSerializer
    lookup_field = "slug"
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_parent_object(self):
        post_slug = self.request.query_params.get("post", None)
        post = get_object_or_404(Post, slug=post_slug, user=self.request.user)

        return post

    def get_object(self, slug: str):
        post = self.get_parent_object()
        photo = get_object_or_404(Photo, slug=slug, post=post)

        return photo

    def perform_list(self, parent):
        return Photo.objects.filter(post=parent)

    def list(self, req: Request):
        parent = self.get_parent_object()
        serializer = self.serializer_class(self.perform_list(parent), many=True)

        return Response(serializer.data)

    def retrieve(self, req: Request, slug: str = None):
        objs = self.get_object(slug)

        return Response(self.serializer_class(objs).data)

    def destroy(self, req: Request, slug: str = None):
        objs = self.get_object(slug)
        objs.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)