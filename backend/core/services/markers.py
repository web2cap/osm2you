import logging

from django.contrib.gis.geos import Point
from django.db.models import Prefetch, Q

from core.models.kinds import Kind
from core.models.markers import Marker
from core.models.stories import Story
from core.models.tags import TagValue

logger = logging.getLogger(__name__)


class MarkerService:
    @staticmethod
    def get_or_create_marker(coordinates, marker_data):
        location = MarkerService._get_location_from_coordinates(coordinates)
        marker, created = Marker.objects.get_or_create(location=location, **marker_data)
        return marker, created

    @staticmethod
    def update_marker(marker, marker_data):
        if "name" in marker_data and marker_data["name"]:
            marker.name = marker_data["name"]
        if "osm_id" in marker_data and marker_data["osm_id"]:
            marker.osm_id = marker_data["osm_id"]
        marker.save()
        return marker

    @staticmethod
    def get_by_id(marker_id):
        try:
            return Marker.objects.get(id=marker_id)
        except Marker.DoesNotExist:
            return None

    @staticmethod
    def get_by_coordinates(coordinates):
        try:
            location = MarkerService._get_location_from_coordinates(coordinates)
            markers = Marker.objects.filter(location=location)
            for marker in markers:
                if marker.location == location:
                    return marker
            return None
        except Exception as e:
            logger.error(f"Error getting marker by coordinates: [{coordinates}] : {e} ")
            return None

    @staticmethod
    def get_markers_all():
        return Marker.objects.all()

    @staticmethod
    def get_markers_main_kind():
        return Marker.objects.filter(kind__kind__kind_class=Kind.KIND_CLASS_MAIN)

    @staticmethod
    def get_markers_with_stories_tags():
        return Marker.objects.select_related("author").prefetch_related(
            Prefetch(
                "stories",
                queryset=Story.objects.select_related("author"),
            ),
            "stories__author",
            Prefetch(
                "tag_value",
                queryset=TagValue.objects.select_related("tag"),
            ),
            "tag_value__tag",
        )

    @staticmethod
    def get_users_markers_stories(user):
        """Get the queryset for markers associated with a specific user and their stories."""
        if not user:
            raise ValueError("No user for gettingß users markers.ß")
        return (
            Marker.objects.filter(
                Q(stories__isnull=False, stories__author=user) | Q(author=user)
            )
            .distinct()
            .prefetch_related(
                Prefetch(
                    "stories",
                    queryset=Story.objects.filter(author=user),
                )
            )
        )

    @staticmethod
    def _get_location_from_coordinates(coordinates):
        return Point(float(coordinates["lon"]), float(coordinates["lat"]))
