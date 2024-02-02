from django.conf import settings
from djoser.serializers import UserCreateSerializer
from markers.models import Marker, MarkerCluster
from rest_framework import serializers
from rest_framework.serializers import ReadOnlyField
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from stories.models import Story
from users.models import User

MARKERS_KIND_MAIN = getattr(settings, "MARKERS_KIND_MAIN")
MARKERS_KIND_RELATED = getattr(settings, "MARKERS_KIND_RELATED")


class CustomUserShortSerializer(UserCreateSerializer):
    """Shot user serializer for display user data in related models."""

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ("id", "first_name", "username")


class CustomUserInfoSerializer(UserCreateSerializer):
    """User serializer for display users data in users page."""

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ("id", "first_name", "username", "date_joined", "bio")


class StorySerializer(serializers.ModelSerializer):
    """Stories serializer."""

    def validate_text(self, value):
        value = value.strip()
        if len(value) < 10:
            raise serializers.ValidationError(
                "Text must be at least 10 characters long."
            )
        return value

    class Meta:
        model = Story
        fields = ("id", "text", "author", "marker")
        read_only_fields = ("id", "author")


class StorySerializerText(serializers.ModelSerializer):
    """Stories serializer for edit. Enable edit text."""

    def validate_text(self, value):
        value = value.strip()
        if len(value) < 10:
            raise serializers.ValidationError(
                "Text must be at least 10 characters long."
            )
        return value

    class Meta:
        model = Story
        fields = ("text", "created")
        read_only_fields = ("created",)


class StorySerializerDisplay(serializers.ModelSerializer):
    """Extendet stories serializer with aditional user info.
    Field is_yours True for owners of record.
    Field marker excludet."""

    author = CustomUserShortSerializer(many=False, read_only=True)
    is_yours = serializers.SerializerMethodField()

    def get_is_yours(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.author_id == request.user.id
        return False

    class Meta:
        model = Story
        fields = ("id", "text", "author", "is_yours", "created")


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


class MarkerInstanceSerializer(MarkerSerializer):
    """Extend MarkerSerializer,  add marker stories and tags with values lists."""

    stories = StorySerializerDisplay(many=True, read_only=True)
    tags = serializers.SerializerMethodField()
    kind = serializers.SerializerMethodField()

    def get_tags(self, obj):
        tags = obj.tag_value.all()
        return {tag.tag.name: tag.value for tag in tags}

    def get_kind(self, obj):
        """If the main kind tag is present with the specified value, return main kind tag value.
        Else if one of MARKERS_KIND_RELATED present with the specified value, return MARKERS_KIND_RELATED main category.
        Else return None."""

        if any(
            tag.tag.name == MARKERS_KIND_MAIN["tag"]
            and tag.value in MARKERS_KIND_MAIN["tag_value"]
            for tag in obj.tag_value.all()
        ):
            return MARKERS_KIND_MAIN["tag_value"]

        for _, config in MARKERS_KIND_RELATED.items():
            for tag_name, tag_values in config["tag"].items():
                if any(
                    tag.tag.name == tag_name and tag.value in tag_values
                    for tag in obj.tag_value.all()
                ):
                    return config["name"]

        return None

    class Meta:
        fields = ("id", "name", "is_yours", "stories", "tags", "kind", "add_date")
        read_only_fields = ("id", "stories", "tags", "kind", "add_date")
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
