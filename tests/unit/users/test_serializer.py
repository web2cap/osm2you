import pytest
from api.serializers.users import CustomUserCreateSerializer, CustomUserFullSerializer


class TestUsersSerializer:
    @pytest.mark.django_db
    def test_user_create_custom_serializer_valid(self, full_create_user_data):
        """Check serialization with valid user data."""

        serializer = CustomUserCreateSerializer(data=full_create_user_data)
        assert (
            serializer.is_valid()
        ), f"Error serialize user with valid data {serializer.errors}"

    @pytest.mark.django_db
    def test_user_create_custom_serializer_invalid(
        self, full_create_user_data_without_email
    ):
        """Check that serializator is not valid with invalid user data."""

        serializer = CustomUserCreateSerializer(
            data=full_create_user_data_without_email
        )
        assert not serializer.is_valid(), "User serialized withot email."

    @pytest.mark.django_db
    def test_user_custom_serializer_no_email(self, full_create_user_data):
        """Check that email not present in dataafter serialization."""

        serializer = CustomUserFullSerializer(full_create_user_data)
        data = serializer.data
        assert "email" not in data, "Email must be read-only"

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        "must_present",
        [
            "username",
            "last_name",
            "first_name",
            "bio",
            "instagram",
            "telegram",
            "facebook",
        ],
    )
    def test_user_custom_serializer_data(self, must_present, full_create_user_data):
        """Check that data valid after serialization."""

        serializer = CustomUserFullSerializer(full_create_user_data)
        data = serializer.data
        assert (
            must_present in data
        ), f"Field {must_present} should present in valid data."
        assert (
            data[must_present] == full_create_user_data[must_present]
        ), f"Wrong {must_present} after serialization"
