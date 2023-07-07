from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("api/", include("markers.api")),
    path("admin/", admin.site.urls),
]
