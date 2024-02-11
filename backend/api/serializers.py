from djoser.serializers import UserCreateSerializer
from markers.models import Marker, MarkerCluster
from rest_framework import serializers
from rest_framework.serializers import ReadOnlyField
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from stories.models import Story
from tags.models import Kind, MarkerKind, Tag
from users.models import User


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


class MarkerRelatedSerializer(MarkerSerializer):
    """Marker GeoJSON serializer with kind field."""

    kind = serializers.SerializerMethodField()

    def get_kind(self, obj):
        try:
            marker_kind = obj.kind
            return f"{marker_kind.kind.tag.name}={marker_kind.kind.value}"
        except MarkerKind.DoesNotExist:
            return None

    class Meta:
        fields = ("id", "name", "is_yours", "kind")
        read_only_fields = ("id", "kind")
        geo_field = "location"
        model = Marker


class MarkerInstanceSerializer(MarkerSerializer):
    """Extend MarkerSerializer,  add marker stories and tags with values lists."""

    stories = StorySerializerDisplay(many=True, read_only=True)
    tags = serializers.SerializerMethodField()
    kind = serializers.SerializerMethodField()
    related = serializers.SerializerMethodField()

    def get_tags(self, obj):
        tags = obj.tag_value.all()
        return {tag.tag.name: tag.value for tag in tags}

    def get_kind(self, obj):
        try:
            marker_kind = obj.kind
            return f"{marker_kind.kind.tag.name}={marker_kind.kind.value}"
        except MarkerKind.DoesNotExist:
            return None

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


class KindSerializer(serializers.ModelSerializer):
    color = serializers.CharField(source="kind_group.color", read_only=True)
    icon = serializers.CharField(source="kind_group.icon", read_only=True)
    tag = serializers.CharField(source="tag.name", read_only=True)
    tag_display_name = serializers.CharField(source="tag.display_name", read_only=True)
    kind = serializers.SerializerMethodField()

    def get_kind(self, obj):
        return f"{obj.tag.name}={obj.value}"

    class Meta:
        model = Kind
        fields = ("tag", "tag_display_name", "value", "color", "icon", "kind")


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            "name",
            "display_name",
        )
