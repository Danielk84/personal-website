from django.urls import path

from .router import SlugPrefixRouter
from . import views

router = SlugPrefixRouter

router.register(r"photos", views.PhotoManagerViewSet, basename="photo")

app_name = "media"
urlpatterns = router.routes