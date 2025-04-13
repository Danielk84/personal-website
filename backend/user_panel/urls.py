from django.urls import path

from . import views

app_name = "user_panel"
urlpatterns = [
    path("login/", views.jwt_login, name="login"),
]