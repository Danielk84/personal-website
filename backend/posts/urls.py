from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register(r"posts", views.PostListViewSet, basename="posts")

app_name = "posts"
urlpatterns = [
    path("post/<slug:slug_value>/", views.get_post, name="post"),
] + router.urls