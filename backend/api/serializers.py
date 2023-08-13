from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from djoser.serializers import UserCreateSerializer, UserSerializer

from markers.models import Marker
from users.models import User


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


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ("email", "password", "first_name", "username")


class CustomUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = User
        fields = (
            "email",
            "first_name",
            "username",
            "bio",
            "instagram",
            "telegram",
            "facebook",
        )
