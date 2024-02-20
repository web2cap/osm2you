import pytest
from api.serializers.users import (
    CustomUserCreateSerializer,
    CustomUserFullSerializer,
    CustomUserInfoSerializer,
    CustomUserShortSerializer,
)


class TestUsersSerializer:
    # CustomUserCreateSerializer
    @pytest.mark.django_db
    def test_custom_user_create_serializer_valid(self, full_create_user_data):
        """Check serialization with valid user data."""

        serializer = CustomUserCreateSerializer(data=full_create_user_data)
        assert (
            serializer.is_valid()
        ), f"Error serialize user with valid data {serializer.errors}"

    @pytest.mark.django_db
    def test_custom_user_create_serializer_invalid(
        self, full_create_user_data_without_email
    ):
        """Check that serializator is not valid with invalid user data."""

        serializer = CustomUserCreateSerializer(
            data=full_create_user_data_without_email
        )
        assert not serializer.is_valid(), "User serialized withot email."

    # CustomUserFullSerializer
    @pytest.mark.django_db
    def test_custom_user_full_serializer_no_email(self, full_create_user_data):
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
    def test_custom_user_full_serializer_data(
        self, must_present, full_create_user_data
    ):
        """Check that data valid after serialization."""

        serializer = CustomUserFullSerializer(full_create_user_data)
        data = serializer.data
        assert (
            must_present in data
        ), f"Field {must_present} should present in valid data."
        assert (
            data[must_present] == full_create_user_data[must_present]
        ), f"Wrong {must_present} after serialization"

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

    # CustomUserInfoSerializer
    @pytest.mark.django_db
    def test_custom_user_info_serializer_valid(self, user_instance):
        """Check serialization with valid user data."""

        serializer = CustomUserInfoSerializer(instance=user_instance)
        assert serializer.data[
            "id"
        ], f"Error serialize user with valid data {serializer.errors}"

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        "must_present",
        ["id", "first_name", "username", "bio"],
    )
    def test_custom_user_info_serializer_data(self, user_instance, must_present):
        """Check that needet data includet."""

        serializer = CustomUserInfoSerializer(instance=user_instance)
        assert (
            must_present in serializer.data
        ), f"Field {must_present} should present in valid data."
        assert serializer.data[must_present] == getattr(
            user_instance, must_present
        ), f"{must_present} in serialized data not eqal user model data"

    @pytest.mark.django_db
    def test_custom_user_info_serializer_date_joined(self, user_instance):
        """Check that needet data includet."""

        serializer = CustomUserInfoSerializer(instance=user_instance)
        assert (
            "date_joined" in serializer.data
        ), "Field date_joined should present in valid data."
        assert (
            serializer.data["date_joined"] == user_instance.date_joined.isoformat()
        ), "date_joined in serialized data not eqal user model data"

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
            "email",
            "instagram",
            "telegram",
            "facebook",
        ],
    )
    def test_custom_user_info_serializer_must_not_present(
        self, user_instance, must_not_present
    ):
        """Check that no extra fields includet."""

        serializer = CustomUserInfoSerializer(instance=user_instance)
        assert (
            must_not_present not in serializer.data
        ), f"Field {must_not_present} should not present in valid data."
