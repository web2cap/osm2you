from rest_framework import viewsets
from rest_framework_gis import filters

from markers.models import Marker
from stories.models import Story
from api.serializers import (
    MarkerSerializer,
    MarkerInstanceSerializer,
    StorySerializer,
    StorySerializerDisplay,
    StorySerializerEdit,
)
from api.permissions import AuthorAdminOrReadOnly, AuthorAdminOrInstanceOnly


class MarkerViewSet(viewsets.ModelViewSet):
    """Marker view set."""

    queryset = Marker.objects.all()
    permission_classes = (AuthorAdminOrReadOnly,)

    bbox_filter_field = "location"
    filter_backends = (filters.InBBoxFilter,)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return MarkerInstanceSerializer
        return MarkerSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class StoryViewSet(viewsets.ModelViewSet):
    """Story view set."""

    queryset = Story.objects.all()
    permission_classes = (AuthorAdminOrInstanceOnly,)
    serializers = {
        "list": StorySerializerDisplay,
        "retrieve": StorySerializerDisplay,
        "partial_update": StorySerializerEdit,
        "default": StorySerializer,
    }

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializers["default"])
