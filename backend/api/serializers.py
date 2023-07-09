from rest_framework_gis import serializers
from djoser.serializers import UserCreateSerializer, UserSerializer

from markers.models import Marker
from users.models import User


class MarkerSerializer(serializers.GeoFeatureModelSerializer):
    """Marker GeoJSON serializer."""

    class Meta:
        fields = ("id", "name")
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
