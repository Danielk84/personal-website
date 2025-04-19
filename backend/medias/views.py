from django.views.static import serve
from rest_framework import viewsets, mixins, permissions
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Photo
from .serializers import PhotoSerializer
from user_panel.auth import JWTAuthentication


class PhotoListForPostViewSet(
    mixins.ListModelMixin,
    viewsets.GeneratorExit,
):
    pass


class PhotoManagerViewSet(
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Retrieves the queryset of photos owned by the authenticated user.

        This method filters the photos in the database to only include those
        that belong to the current user making the request.

        Returns:
            QuerySet: A QuerySet of photos owned by the authenticated user.
        """
        return Photo.objects.filter(user=self.request.user)