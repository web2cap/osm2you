from core.models.markers import Marker, MarkerCluster
from rest_framework import serializers
from rest_framework.serializers import ReadOnlyField
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from api.serializers.stories import StorySerializerDisplay, StorySerializerText


class MarkerSerializer(GeoFeatureModelSerializer):
    """Marker GeoJSON serializer."""

    is_yours = serializers.SerializerMethodField()

    def get_is_yours(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.author_id == request.user.id
        return False

    class Meta:
        fields = ("id", "name", "is_yours")
        read_only_fields = ("id",)
        geo_field = "location"
        model = Marker


class MarkerRelatedSerializer(MarkerSerializer):
    """Marker GeoJSON serializer with kind field."""

    # kind = serializers.SerializerMethodField()
    #
    # def get_kind(self, obj):
    #     try:
    #         marker_kind = obj.kind
    #         return f"{marker_kind.kind.tag.name}={marker_kind.kind.value}"
    #     except MarkerKind.DoesNotExist:
    #         return None

    class Meta:
        fields = ("id", "name", "is_yours", "kind")
        read_only_fields = ("id", "kind")
        geo_field = "location"
        model = Marker


class MarkerInstanceSerializer(MarkerSerializer):
    """Extend MarkerSerializer,  add marker stories and tags with values lists."""

    stories = StorySerializerDisplay(many=True, read_only=True)
    tags = serializers.SerializerMethodField()
    # kind = serializers.SerializerMethodField()
    related = serializers.SerializerMethodField()

    def get_tags(self, obj):
        tags = obj.tag_value.all()
        return {tag.tag.name: tag.value for tag in tags}

    # def get_kind(self, obj):
    #     try:
    #         marker_kind = obj.kind
    #         return f"{marker_kind.kind.tag.name}={marker_kind.kind.value}"
    #     except MarkerKind.DoesNotExist:
    #         return None

    def get_related(self, obj):
        related_markers_data = self.context.get("related_markers")
        return related_markers_data

    class Meta:
        fields = (
            "id",
            "name",
            "is_yours",
            "stories",
            "tags",
            "kind",
            "related",
            "add_date",
        )
        read_only_fields = (
            "id",
            "stories",
            "tags",
            "kind",
            "related",
            "add_date",
        )
        geo_field = "location"
        model = Marker


class MarkerUserSerializer(GeoFeatureModelSerializer):
    """Serializer for user stories and markers."""

    stories = StorySerializerText(many=True, read_only=True)

    class Meta:
        fields = ("id", "name", "stories")
        geo_field = "location"
        model = Marker


class MarkerClusterSerializer(GeoFeatureModelSerializer):
    """Marker Cluster GeoJSON serializer."""

    kind = ReadOnlyField(default="cluster")

    class Meta:
        fields = ("id", "markers_count", "kind")
        read_only_fields = ("id", "markers_count", "kind")
        geo_field = "location"
        model = MarkerCluster
