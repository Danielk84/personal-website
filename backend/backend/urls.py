from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("posts.urls")),
    path('admin/', admin.site.urls),
    path("user-panel/", include("user_panel.urls")),
    path("medias/", include("medias.urls"))
]