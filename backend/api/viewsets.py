from rest_framework import viewsets
from rest_framework_gis import filters

from markers.models import Marker
from stories.models import Story
from api.serializers import MarkerSerializer, StorySerializer
from api.permissions import AuthorAdminOrReadOnly


class MarkerViewSet(viewsets.ModelViewSet):
    """Marker view set."""

    queryset = Marker.objects.all()
    serializer_class = MarkerSerializer
    permission_classes = (AuthorAdminOrReadOnly,)

    bbox_filter_field = "location"
    filter_backends = (filters.InBBoxFilter,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class StoryViewSet(viewsets.ModelViewSet):
    """Story view set."""

    queryset = Story.objects.all()
    serializer_class = StorySerializer
