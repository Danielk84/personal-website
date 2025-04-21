from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()

router.register(
    "post-activation", views.PostActicationViewSet, basename="post-activation",
)
router.register(
    "photo-activation", views.PhototActivationViewSet, basename="photo-activation",
)

app_name = "user_panel"
urlpatterns = [
    path("login/", views.jwt_login, name="login"),
] + router.urls