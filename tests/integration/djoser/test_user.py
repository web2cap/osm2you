import pytest
from users.models import User

from ..common import check_response


class TestUser:
    """Integration test for user create, read.
    Test that disabled methods are disabled."""

    URL_USERS = "/api/v1/auth/users/"
    URL_USERS_ME = "/api/v1/auth/users/me/"

    # CREATE
    @pytest.mark.django_db()
    def test_user_create_nodata(self, client):
        response = client.post(self.URL_USERS)
        check_response(response, 400, ["email", "password", "first_name"])

    @pytest.mark.parametrize(
        "exclude_field",
        [
            "email",
            "password",
            "first_name",
        ],
    )
    @pytest.mark.django_db()
    def test_user_create_no_requaried_data(
        self, client, full_create_user_data, exclude_field
    ):
        """Test create user with invalid data doesn't created."""

        full_create_user_data.pop(exclude_field)
        response = client.post(self.URL_USERS, data=full_create_user_data)
        check_response(response, 400, [exclude_field])

    @pytest.mark.django_db()
    def test_user_create_invalid_email(self, client, full_create_user_data):
        """Test create user with invalid data doesn't created."""

        full_create_user_data["email"] = "invalid.email"
        response = client.post(self.URL_USERS, data=full_create_user_data)
        check_response(response, 400, ["email"])

    @pytest.mark.django_db()
    def test_user_create_not_unic_data(
        self, client, user_owner_instance, sample_user_data_not_unique_username
    ):
        """Test create user with invalid data doesn't created."""

        response = client.post(
            self.URL_USERS, data=sample_user_data_not_unique_username
        )
        check_response(response, 400, ["email"])

    @pytest.mark.django_db()
    def test_user_create_valid_data(self, client, full_create_user_data):
        response = client.post(self.URL_USERS, data=full_create_user_data)
        requaried_fields = [
            "email",
            "username",
            "last_name",
            "first_name",
            "bio",
            "instagram",
            "telegram",
            "facebook",
        ]
        check_response(response, 201, requaried_fields)

        new_user = User.objects.filter(email=full_create_user_data["email"])
        assert new_user.exists(), (
            f"Check that after request `{self.URL_USERS}` with valid data"
            f" there is the record with this user in the database"
        )

    # ME GET
    @pytest.mark.django_db()
    def test_user_me_unautorized(self, client):
        response = client.post(self.URL_USERS_ME)
        check_response(response, 401, ["detail"])
