from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()

router.register(r"photos", views.PhotoManagerViewSet, basename="photo")

app_name = "media"
urlpatterns = router.urls