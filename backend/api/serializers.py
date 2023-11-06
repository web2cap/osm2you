from djoser.serializers import UserCreateSerializer
from markers.models import Marker
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from stories.models import Story
from users.models import User


class CustomUserShortSerializer(UserCreateSerializer):
    """Shot user serializer for display user data in related models."""

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ("id", "first_name", "username")


class StorySerializer(serializers.ModelSerializer):
    """Stories serializer."""

    class Meta:
        model = Story
        fields = ("id", "text", "author", "marker")


class StorySerializerEdit(serializers.ModelSerializer):
    """Stories serializer for edit. Enable edit text."""

    class Meta:
        model = Story
        fields = ("text",)


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
        fields = ("id", "text", "author", "is_yours")


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
    """Extend MarkerSerializer,  add marker stories list."""

    stories = StorySerializerDisplay(many=True, read_only=True)

    class Meta:
        fields = ("id", "name", "is_yours", "stories")
        read_only_fields = ("id", "stories")
        geo_field = "location"
        model = Marker
