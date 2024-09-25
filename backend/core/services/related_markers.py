from api.serializers.markers import MarkerRelatedSerializer
from django.conf import settings
from django.db.models import Prefetch

from core.models.markers import Marker
from core.models.tags import Tag

MARKERS_RELATED_IN_RADIUS = getattr(settings, "MARKERS_RELATED_IN_RADIUS", 5000)


class RelatedMarkers:
    @staticmethod
    def _get_related_markers_queryset(marker, radius_meters):
        """
        Get the queryset for related markers within a specified radius from a given marker.
        Each related marker includes additional information about its kind."""

        # Convert meters to degrees for the radius
        radius_degrees = RelatedMarkers._convert_meters_to_degrees(radius_meters)

        return (
            Marker.objects.filter(location__dwithin=(marker.location, radius_degrees))
            .exclude(id=marker.id)
            .select_related("kind")
            .prefetch_related(
                Prefetch(
                    "kind__tag",
                    queryset=Tag.objects.only("name"),
                )
            )
        )

    @staticmethod
    def _convert_meters_to_degrees(meters):
        """Convert miles to degrees."""

        return meters / 40000000 * 360

    @staticmethod
    def get_related_markers_data(marker):
        """Get related markers data for a given marker within a specified radius."""

        related_markers = RelatedMarkers._get_related_markers_queryset(
            marker, MARKERS_RELATED_IN_RADIUS
        )
        return MarkerRelatedSerializer(related_markers, many=True).data
