from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from medias.views import server_photo

urlpatterns = [
    path("", include("posts.urls")),
    path('admin/', admin.site.urls),
    path("user-panel/", include("user_panel.urls")),
    path("medias/", include("medias.urls")),
    path(
        "md_files/<path:path>",
        server_photo,
        {"document_root": settings.MEDIA_ROOT },
    ),
]