from http import HTTPMethod

from django.contrib.auth import authenticate
from rest_framework import status, viewsets, permissions, mixins
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from .auth import generate_token, OnlyAdminJWTAuthetication
from .serializers import (
    UserLoginSerializer,
    create_activation_serializer,
    create_full_serializer,
)
from posts.models import Post
from medias.models import Photo


@api_view([HTTPMethod.POST])
def jwt_login(req: Request):
    try:
        data = UserLoginSerializer(data=req.data)
        if not data.is_valid():
            return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)

        assert (user := authenticate(
            username=data.validated_data["username"],
            password=data.validated_data["password"],
        ))
        token = generate_token(user)

        return Response({"Token": token})
    except Exception:
        return Response(status=status.HTTP_403_FORBIDDEN)


class AdminManagerMixin(
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
):
    queryset = ...
    lookup_field = "slug"
    authentication_classes = [OnlyAdminJWTAuthetication]
    permission_classes = [permissions.IsAuthenticated]
    full_serializer = ...

    def retrieve(self, slug: str):
        try:
            obj = self.queryset.get(slug=slug)
            return Response(self.full_serializer(obj).data)
        except Exception:
            return Response(status=status.HTTP_404_NOT_FOUND)


class PostActicationViewSet(AdminManagerMixin, viewsets.GenericViewSet):
    queryset = Post.objects.order_by("is_active")
    serializer_class = create_activation_serializer(Post)
    full_serializer = create_full_serializer(Post)


class PhototActivationViewSet(AdminManagerMixin, viewsets.GenericViewSet):
    queryset = Photo.objects.order_by("is_active")
    serializer_class = create_activation_serializer(Photo)
    full_serializer = create_full_serializer(Photo)