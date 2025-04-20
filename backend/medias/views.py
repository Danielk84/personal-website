from django.views.static import serve
from rest_framework import viewsets, permissions, exceptions
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Photo
from .serializers import PhotoSerializer
from user_panel.auth import JWTAuthentication


class PhotoListForPostViewSet(viewsets.ViewSet):
    pass


class PhotoManagerViewSet(viewsets.ViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "slug"