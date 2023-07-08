from django.urls import include, path
from rest_framework import routers

# from .views import
from .viewsets import MarkerViewSet

app_name = "api"

router = routers.DefaultRouter()
router.register("markers", MarkerViewSet, basename="markers")


urlpatterns = [
    path("", include(router.urls)),
]
