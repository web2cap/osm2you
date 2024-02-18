from django.contrib.gis.geos import Point

from core.models.markers import Marker


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
        except Exception as e:
            return False

    @staticmethod
    def get_by_coordinates(coordinates):
        try:
            return Marker.objects.get(
                location=MarkerService._get_location_from_coordinates(coordinates)
            )
        except Exception as e:
            return False

    @staticmethod
    def _get_location_from_coordinates(coordinates):
        return Point(float(coordinates["lon"]), float(coordinates["lat"]))
