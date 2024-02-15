from django.contrib.gis.geos import Point

from core.models.markers import Marker


class MarkerService:
    @staticmethod
    def get_or_create_marker(coordinates, marker_data):

        location = Point(float(coordinates["lon"]), float(coordinates["lat"]))
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
