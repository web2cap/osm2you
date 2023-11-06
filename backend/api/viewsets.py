from django.db.models import Prefetch
from markers.models import Marker
from rest_framework import viewsets
from rest_framework_gis import filters
from stories.models import Story

from api.permissions import AuthorAdminOrInstanceOnly, AuthorAdminOrReadOnly
from api.serializers import (
    MarkerInstanceSerializer,
    MarkerSerializer,
    StorySerializer,
    StorySerializerDisplay,
    StorySerializerEdit,
)


class MarkerViewSet(viewsets.ModelViewSet):
    """Marker view set."""

    permission_classes = (AuthorAdminOrReadOnly,)

    bbox_filter_field = "location"
    filter_backends = (filters.InBBoxFilter,)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return MarkerInstanceSerializer
        return MarkerSerializer

    def get_queryset(self):
        queryset = Marker.objects.all()
        if self.action == "retrieve":
            queryset = queryset.prefetch_related(
                Prefetch(
                    "stories",
                    queryset=Story.objects.select_related("author"),
                ),
                "stories__author",
            )
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class StoryViewSet(viewsets.ModelViewSet):
    """Story view set."""

    queryset = Story.objects.select_related("author").all()
    serializer_class = StorySerializer
    permission_classes = (AuthorAdminOrInstanceOnly,)
    serializers = {
        "list": StorySerializerDisplay,
        "retrieve": StorySerializerDisplay,
        "partial_update": StorySerializerEdit,
        "default": StorySerializer,
    }

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializers["default"])
