from rest_framework_gis import serializers

from markers.models import Marker


class MarkerSerializer(serializers.GeoFeatureModelSerializer):
    """Marker GeoJSON serializer."""

    class Meta:

        fields = ("id", "name")
        geo_field = "location"
        model = Marker
