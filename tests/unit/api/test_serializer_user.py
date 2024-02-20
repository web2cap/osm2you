import pytest
from api.serializers.users import CustomUserShortSerializer


class TestApiSerializer:
    """Test user, markers, stories serizlizers."""

    # CustomUserShortSerializer
    @pytest.mark.django_db
    def test_custom_user_short_serializer_valid(self, user_instance):
        """Check serialization with valid user data."""

        serializer = CustomUserShortSerializer(instance=user_instance)
        assert serializer.data[
            "id"
        ], f"Error serialize user with valid data {serializer.errors}"

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        "must_present",
        [
            "id",
            "first_name",
            "username",
        ],
    )
    def test_custom_user_short_serializer_data(self, user_instance, must_present):
        """Check that needet data includet."""

        serializer = CustomUserShortSerializer(instance=user_instance)
        assert (
            must_present in serializer.data
        ), f"Field {must_present} should present in valid data."
        assert serializer.data[must_present] == getattr(
            user_instance, must_present
        ), f"{must_present} in serialized data not eqal user model data"

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        "must_not_present",
        [
            "password",
            "last_login",
            "is_superuser",
            "last_name",
            "is_staff",
            "is_active",
            "date_joined",
            "email",
            "bio",
            "instagram",
            "telegram",
            "facebook",
        ],
    )
    def test_custom_user_short_serializer_must_not_present(
        self, user_instance, must_not_present
    ):
        """Check that no extra fields includet."""

        serializer = CustomUserShortSerializer(instance=user_instance)
        assert (
            must_not_present not in serializer.data
        ), f"Field {must_not_present} should not present in valid data."
