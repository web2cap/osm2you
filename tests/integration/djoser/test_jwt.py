import pytest


class TestJwt:
    """Integration test for token create, refresh."""

    URL_CREATE_TOKEN = "/api/v1/auth/jwt/create/"
    URL_REFRESH_TOKEN = "/api/v1/auth/jwt/refresh/"

    # CREATE
    @pytest.mark.django_db()
    def test_token_create_nodata(self, client):
        response = client.post(self.URL_CREATE_TOKEN)
        assert (
            response.status_code != 404
        ), f"Page `{self.URL_CREATE_TOKEN}` not found, check address in *urls.py*"
        code = 400
        assert response.status_code == code, (
            f"Check that request `{self.URL_CREATE_TOKEN}` without parameters"
            f"user is not created and status is returned {code}"
        )
        response_json = response.json()
        empty_fields = ["email", "password"]
        for field in empty_fields:
            assert field in response_json.keys() and isinstance(
                response_json[field], list
            ), (
                f"Check that request `{self.URL_CREATE_TOKEN}` without parameters"
                f"in the response there is a message about filled {field}"
            )

    @pytest.mark.django_db()
    def test_token_create_invalid_data(self, client, sample_user_data, user_instance):
        """Test create token with data, but without creation user with this data."""

        response = client.post(self.URL_CREATE_TOKEN, data=sample_user_data)

        assert (
            response.status_code != 404
        ), f"Page `{self.URL_CREATE_TOKEN}` not found, check address in *urls.py*"
        code = 401
        assert response.status_code == 401, (
            f"Check that request `{self.URL_CREATE_TOKEN}` with invalid data "
            f"user is not created and status is returned {code}"
        )

        response_json = response.json()
        assert "detail" in response_json.keys() and response_json["detail"], (
            f"Check that request `{self.URL_CREATE_TOKEN}` with invalid parameters, "
            f"in the response there is a message about field `detail`"
        )

        valid_data_no_password = {
            "email": user_instance.email,
        }
        response = client.post(self.URL_CREATE_TOKEN, data=valid_data_no_password)
        code = 400
        assert response.status_code == code, (
            f"Check that request `{self.URL_CREATE_TOKEN}` without username "
            f"cannot create user and return status {code}"
        )

    @pytest.mark.django_db(transaction=True)
    def test_token_create_valid_data(
        self, client, full_create_user_data, user_instance
    ):
        auth_data = {
            "email": full_create_user_data["email"],
            "password": full_create_user_data["password"],
        }
        response = client.post(self.URL_CREATE_TOKEN, data=auth_data)

        assert (
            response.status_code != 404
        ), f"Page `{self.URL_CREATE_TOKEN}` not found, check this address in *urls.py*"

        code = 200
        assert response.status_code == code, (
            f"Check that request `{self.URL_CREATE_TOKEN}` with valid data"
            f"user is created and status is returned {code}"
        )

        response_json = response.json()
        requaried_fields = ["refresh", "access"]
        for field in requaried_fields:
            assert field in response_json.keys() and len(response_json[field]), (
                f"Check that request `{self.URL_CREATE_TOKEN}` with valid data"
                f"in the response there is a filled {field}"
            )

    # REFRESH
