from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()

router.register("photos", views.PhotoManagerViewSet, basename="photo")
router.register("upload-photo", views.UploadPhotoViewSet, basename="upload-photo")

app_name = "media"
urlpatterns = router.urls