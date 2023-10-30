import pytest

from ..common import check_response


class TestJwt:
    """Integration test for token create, refresh."""

    URL_CREATE_TOKEN = "/api/v1/auth/jwt/create/"
    URL_REFRESH_TOKEN = "/api/v1/auth/jwt/refresh/"

    # CREATE
    @pytest.mark.django_db()
    def test_token_create_nodata(self, client):
        response = client.post(self.URL_CREATE_TOKEN)
        check_response(response, 400, ["email", "password"])

    @pytest.mark.django_db()
    def test_token_create_invalid_data(self, client, sample_user_data, user_instance):
        """Test create token with data, but without creation user with this data."""

        response = client.post(self.URL_CREATE_TOKEN, data=sample_user_data)
        check_response(response, 401, ["detail"])

        valid_data_no_password = {
            "email": user_instance.email,
        }
        response = client.post(self.URL_CREATE_TOKEN, data=valid_data_no_password)
        check_response(response, 400, ["password"])

    @pytest.mark.django_db(transaction=True)
    def test_token_create_valid_data(
        self, client, full_create_user_data, user_instance
    ):
        auth_data = {
            "email": full_create_user_data["email"],
            "password": full_create_user_data["password"],
        }
        response = client.post(self.URL_CREATE_TOKEN, data=auth_data)
        check_response(response, 200, ["refresh", "access"])

    # REFRESH
    @pytest.mark.django_db()
    def test_token_refresh_nodata(self, client):
        response = client.post(self.URL_REFRESH_TOKEN)
        check_response(response, 400, ["refresh"])

    @pytest.mark.django_db()
    def test_token_refresh_invalid_data(self, client, user_instance):
        """Test create token with data, but without creation user with this data."""

        response = client.post(self.URL_REFRESH_TOKEN, data={"refresh": "Invalid"})
        check_response(response, 401, ["detail"])

    @pytest.mark.django_db(transaction=True)
    def test_token_refresh_valid_data(self, client, user_token):
        response = client.post(
            self.URL_REFRESH_TOKEN, data={"refresh": user_token["refresh"]}
        )
        check_response(response, 200, ["access"])
