from core.models.users import User
from djoser.serializers import UserCreateSerializer, UserSerializer


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "last_name",
            "first_name",
            "bio",
            "instagram",
            "telegram",
            "facebook",
            "password",
        )


class CustomUserFullSerializer(UserSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "last_name",
            "first_name",
            "bio",
            "instagram",
            "telegram",
            "facebook",
        )
        read_only_fields = ("email",)


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
