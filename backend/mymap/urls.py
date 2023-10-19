from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("api/v1/", include("api.urls"), name="api"),
    path("admin/", admin.site.urls, name="admin"),
]

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
