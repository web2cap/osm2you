from djoser import serializers

from .models import User


class UserCreateCustomSerializer(serializers.UserCreateSerializer):
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


class UserCustomSerializer(serializers.UserSerializer):
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
