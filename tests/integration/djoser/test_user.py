import pytest
from users.models import User


class TestUser:
    """Integration test for user create, read.
    Test that disabled methods are disabled."""

    URL_USERS = "/api/v1/auth/users/"
    URL_USERS_ME = "/api/v1/auth/users/me/"

    # CREATE
    @pytest.mark.django_db()
    def test_user_create_nodata(self, client):
        response = client.post(self.URL_USERS)
        assert (
            response.status_code != 404
        ), f"Page `{self.URL_USERS}` not found, check address in *urls.py*"
        code = 400
        assert response.status_code == code, (
            f"Check that request `{self.URL_USERS}` without parameters"
            f"user is not created and status is returned {code}"
        )
        response_json = response.json()
        empty_fields = ["email", "password", "first_name"]
        for field in empty_fields:
            assert field in response_json.keys() and isinstance(
                response_json[field], list
            ), (
                f"Check that request `{self.URL_USERS}` without parameters"
                f"in the response there is a message about filled {field}"
            )

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

        assert (
            response.status_code != 404
        ), f"Page `{self.URL_USERS}` not found, check address in *urls.py*"
        code = 400
        assert response.status_code == code, (
            f"Check that request `{self.URL_USERS}` with invalid data "
            f" user is not created and status is returned {code}"
        )

        response_json = response.json()
        assert exclude_field in response_json.keys() and isinstance(
            response_json[exclude_field], list
        ), (
            f"Check that request `{self.URL_USERS}` with invalid parameters, "
            f"in the response there is a message about field `{exclude_field}`"
        )

    @pytest.mark.django_db()
    def test_user_create_invalid_email(self, client, full_create_user_data):
        """Test create user with invalid data doesn't created."""

        full_create_user_data["email"] = "invalid.email"
        response = client.post(self.URL_USERS, data=full_create_user_data)

        assert (
            response.status_code != 404
        ), f"Page `{self.URL_USERS}` not found, check address in *urls.py*"
        code = 400
        assert response.status_code == code, (
            f"Check that request `{self.URL_USERS}` with invalid data "
            f" user is not created and status is returned {code}"
        )

        response_json = response.json()
        assert "email" in response_json.keys() and isinstance(
            response_json["email"], list
        ), (
            f"Check that request `{self.URL_USERS}` with invalid parameters, "
            f"in the response there is a message about field `email`"
        )

    @pytest.mark.django_db()
    def test_user_create_not_unic_data(
        self, client, user_owner_instance, sample_user_data_not_unique_username
    ):
        """Test create user with invalid data doesn't created."""

        response = client.post(
            self.URL_USERS, data=sample_user_data_not_unique_username
        )

        assert (
            response.status_code != 404
        ), f"Page `{self.URL_USERS}` not found, check address in *urls.py*"
        code = 400
        assert response.status_code == code, (
            f"Check that request `{self.URL_USERS}` with invalid data "
            f" user is not created and status is returned {code}"
        )

        response_json = response.json()
        assert "email" in response_json.keys() and isinstance(
            response_json["email"], list
        ), (
            f"Check that request `{self.URL_USERS}` with invalid parameters, "
            f"in the response there is a message about field `email`"
        )

    @pytest.mark.django_db(transaction=True)
    def test_user_create_valid_data(self, client, full_create_user_data):
        response = client.post(self.URL_USERS, data=full_create_user_data)

        assert (
            response.status_code != 404
        ), f"Page `{self.URL_USERS}` not found, check this address in *urls.py*"

        code = 201
        assert response.status_code == code, (
            f"Check that request `{self.URL_USERS}` with valid data"
            f"user is created and status is returned {code}"
        )

        response_json = response.json()
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
        for field in requaried_fields:
            assert field in response_json.keys(), (
                f"Check that request `{self.URL_USERS}` with valid data"
                f"in the response there is a filled {field}"
            )

        new_user = User.objects.filter(email=full_create_user_data["email"])
        assert new_user.exists(), (
            f"Check that after request `{self.URL_USERS}` with valid data"
            f" there is the record with this user in the database"
        )
