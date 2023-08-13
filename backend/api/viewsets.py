"""Markers API views."""
from rest_framework import viewsets
from rest_framework_gis import filters

from markers.models import Marker
from api.serializers import MarkerSerializer
from api.permissions import AuthorAdminOrReadOnly


class MarkerViewSet(viewsets.ModelViewSet):
    """Marker view set."""

    queryset = Marker.objects.all()
    serializer_class = MarkerSerializer
    permission_classes = (AuthorAdminOrReadOnly,)

    bbox_filter_field = "location"
    filter_backends = (filters.InBBoxFilter,)
