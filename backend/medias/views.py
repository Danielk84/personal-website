from django.views.static import serve
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.parsers import MultiPartParser, FileUploadParser, FormParser
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Photo
from .forms import UploadPhotoForm
from .serializers import PhotoSerializer
from backend.celery import delete_local_file
from user_panel.auth import JWTAuthentication
from posts.models import Post


class BaseGetObjMixin:
    def get_parent_object(self):
        """
        Retrieves the parent post based on the `post` query parameter.

        - Ensures the post belongs to the authenticated user.
        - Returns a 404 error if the post is not found.
        """
        post_slug = self.request.query_params.get("post", None)
        post = get_object_or_404(Post, slug=post_slug, user=self.request.user)

        return post

    def get_object(self, slug: str):
        """
        Retrieves a photo linked to the authenticated user's post.

        - Ensures the photo belongs to the user's post.
        - Raises a 404 error if the photo is missing.
        """
        post = self.get_parent_object()
        photo = get_object_or_404(Photo, slug=slug, post=post)

        return photo


class PhotoManagerViewSet(BaseGetObjMixin, viewsets.ViewSet):
    """
    A viewset for managing photo resources linked to posts.

    This viewset ensures that:
    - Photos are associated with a specific parent post.
    - Users can retrieve, list, and delete photos within their own posts.
    - Only authenticated users with proper permissions can access the API.

    **Authentication & Permissions:**
    - Uses JWT authentication (`authentication_classes`).
    - Requires users to be logged in (`permissions.IsAuthenticated`).
    - Ensures users can only interact with photos linked to their posts.

    **Lookup & Parent Object Handling:**
    - Photos are accessed via their `slug` (defined in `lookup_field`).
    - The `post` query parameter is required to identify the parent post.
    - Methods ensure the user only accesses their own posts and photos.
    """
    serializer_class = PhotoSerializer
    lookup_field = "slug"
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

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


class UploadPhotoViewSet(BaseGetObjMixin, viewsets.ViewSet):
    lookup_field = "slug"
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FileUploadParser, FormParser]

    def create(self, req: Request):
        parent = self.get_parent_object()
        form = UploadPhotoForm(req.data, req.FILES)

        if not form.is_valid():
            return Response(form.errors.as_json(), status=status.HTTP_400_BAD_REQUEST)

        form.save(parent=parent)

        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, req: Request, slug: str):
        obj = self.get_object(slug)
        form = UploadPhotoForm(req.data, req.FILES, instance=obj)

        if not form.is_valid():
            return Response(form.errors.as_json(), status=status.HTTP_400_BAD_REQUEST)

        delete_local_file.delay(obj.img.path)
        form.save()

        return Response(status=status.HTTP_204_NO_CONTENT)