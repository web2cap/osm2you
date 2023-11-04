import pytest
from users.models import User

from .common import check_response


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
    def test_user_create_no_required_data(
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
        required_fields = [
            "email",
            "username",
            "last_name",
            "first_name",
            "bio",
            "instagram",
            "telegram",
            "facebook",
        ]
        check_response(response, 201, required_fields)

        new_user = User.objects.filter(email=full_create_user_data["email"])
        assert new_user.exists(), (
            f"Check that after request `{self.URL_USERS}` with valid data"
            f" there is the record with this user in the database"
        )

    # ME GET
    @pytest.mark.django_db()
    def test_user_me_get_unauthorized(self, client):
        response = client.post(self.URL_USERS_ME)
        check_response(response, 401, ["detail"])

    @pytest.mark.django_db()
    def test_user_me_get_authorized(self, user_client, user_instance):
        response = user_client.get(self.URL_USERS_ME)
        required_fields = [
            "username",
            "last_name",
            "first_name",
            "instagram",
            "telegram",
            "facebook",
        ]
        check_response(response, 200, required_fields)
        for field in response.data.keys():
            assert response.data[field] == getattr(
                user_instance, field
            ), f"The response data[{field}] doesn't match the client user data `{field}`."

    # ME PUT
    @pytest.mark.django_db()
    def test_user_me_put_unauthorized(self, client, full_update_user_data):
        response = client.put(self.URL_USERS_ME, data=full_update_user_data)
        check_response(response, 401, ["detail"])

    @pytest.mark.django_db()
    def test_user_me_put_authorized_empty_data(self, user_client):
        response = user_client.put(self.URL_USERS_ME, data={})
        check_response(response, 400, ["first_name"])

    @pytest.mark.django_db()
    @pytest.mark.parametrize("required_field", ["first_name", "username"])
    def test_user_me_put_authorized_no_required_field(
        self, user_client, full_update_user_data, required_field
    ):
        full_update_user_data.pop(required_field)
        response = user_client.put(self.URL_USERS_ME, data=full_update_user_data)
        check_response(response, 400, [required_field])

    @pytest.mark.django_db()
    def test_user_me_put_authorized_username_exist(
        self, user_client, full_update_user_data, user_owner_instance
    ):
        full_update_user_data["username"] = user_owner_instance.username
        response = user_client.put(self.URL_USERS_ME, data=full_update_user_data)
        check_response(response, 400, ["username"])

    @pytest.mark.django_db()
    def test_user_me_put_authorized_valid_data(
        self, user_client, full_update_user_data
    ):
        response = user_client.put(self.URL_USERS_ME, data=full_update_user_data)

        required_fields = [
            "username",
            "last_name",
            "first_name",
            "instagram",
            "telegram",
            "facebook",
            "bio",
        ]
        check_response(response, 200, required_fields)
        for field in response.data.keys():
            assert (
                response.data[field] == full_update_user_data[field]
            ), f"The response data[{field}] doesn't match the client user data `{field}`."

    # Disabled methods
    @pytest.mark.django_db()
    @pytest.mark.parametrize(
        "url, http_verb, expected_code, required_fields",
        [
            (URL_USERS, "get", 401, ["detail"]),
            (URL_USERS_ME, "patch", 401, ["detail"]),
            (URL_USERS_ME, "delete", 401, ["detail"]),
            (f"{URL_USERS}reset_email/", "post", 401, ["detail"]),
            (f"{URL_USERS}set_email/", "post", 401, ["detail"]),
            (f"{URL_USERS}set_password/", "post", 401, ["detail"]),
        ],
    )
    def test_user_disabled_methods_unauthorized(
        self, client, url, http_verb, expected_code, required_fields
    ):
        action = getattr(client, http_verb)
        response = action(self.URL_USERS)
        check_response(response, expected_code, required_fields)

    @pytest.mark.django_db()
    @pytest.mark.parametrize(
        "url, http_verb, expected_code, required_fields",
        [
            (URL_USERS, "get", 404, ["detail"]),
            (URL_USERS_ME, "patch", 403, ["detail"]),
            (URL_USERS_ME, "delete", 403, ["detail"]),
            (f"{URL_USERS}reset_email/", "post", 401, ["detail"]),
            (f"{URL_USERS}set_email/", "post", 401, ["detail"]),
        ],
    )
    def test_user_disabled_methods_user(
        self, user_client, url, http_verb, expected_code, required_fields
    ):
        action = getattr(user_client, http_verb)
        response = action(self.URL_USERS)
        check_response(response, expected_code, required_fields)
