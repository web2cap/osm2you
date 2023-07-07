"""mymap URL Configuration."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("markers.urls", namespace="markers")),
    path("api/", include("markers.api")),
    path("stories/", include("stories.urls", namespace="stories")),
    path("auth/", include("users.urls", namespace="users")),
    path("auth/", include("django.contrib.auth.urls")),
    path("admin/", admin.site.urls),
]
