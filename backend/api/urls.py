from django.urls import include, path
from djoser.views import TokenCreateView
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from .viewsets import MarkerViewSet

app_name = "api"

router = routers.DefaultRouter()
router.register("markers", MarkerViewSet, basename="markers")


urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include("djoser.urls")),
    path("auth/token/", TokenCreateView.as_view(), name="token_create"),
    path(
        "auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),
]
