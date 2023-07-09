from django.urls import include, path
from rest_framework import routers
from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view

from .viewsets import MarkerViewSet
from .api_info import api_info

app_name = "api"

router = routers.DefaultRouter()
router.register("markers", MarkerViewSet, basename="markers")

schema_view = get_schema_view(
    api_info,
    public=True,
    permission_classes=[AllowAny],
)

urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    path(
        "docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="api-docs",
    ),
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="api-redoc",
    ),
]
