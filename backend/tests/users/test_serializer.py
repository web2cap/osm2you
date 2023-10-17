import pytest

from users.serializers import UserCreateCustomSerializer, UserCustomSerializer


class TestUsersSerializer:
    @pytest.mark.django_db
    def test_user_create_custom_serializer_valid(self, full_create_user_data):
        """Check serialization with valid user data."""

        serializer = UserCreateCustomSerializer(data=full_create_user_data)
        assert serializer.is_valid(), "Error serialize user with valid data"
        print(serializer.errors)

    @pytest.mark.django_db
    def test_user_create_custom_serializer_invalid(
        self, full_create_user_data_without_email
    ):
        """Check that serializator is not valid with invalid user data."""

        serializer = UserCreateCustomSerializer(
            data=full_create_user_data_without_email
        )
        assert not serializer.is_valid(), "User serialized withot email."

    @pytest.mark.django_db
    def test_user_custom_serializer(self, full_create_user_data):
        """Check that data is valid after serialization."""

        serializer = UserCustomSerializer(full_create_user_data)
        data = serializer.data
        assert "email" not in data, "Email must be read-only"
        assert (
            data["username"] == full_create_user_data["username"]
        ), "Wrong username after serialization"
        assert (
            data["first_name"] == full_create_user_data["first_name"]
        ), "Wrong first_name after serialization"
        assert (
            data["last_name"] == full_create_user_data["last_name"]
        ), "Wrong last_name after serialization"
        assert (
            data["bio"] == full_create_user_data["bio"]
        ), "Wrong bio after serialization"
        assert (
            data["instagram"] == full_create_user_data["instagram"]
        ), "Wrong instagram after serialization"
        assert (
            data["telegram"] == full_create_user_data["telegram"]
        ), "Wrong telegram after serialization"
        assert (
            data["facebook"] == full_create_user_data["facebook"]
        ), "Wrong facebook after serialization"
