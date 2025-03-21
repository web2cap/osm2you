import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest
from rest_framework.request import Request
from rest_framework.test import APIClient
from rest_framework.viewsets import ViewSet
from rest_framework_simplejwt.tokens import AccessToken

User = get_user_model()

URL_CREATE_TOKEN = "/api/v1/auth/jwt/create/"


@pytest.fixture
def custom_user_manager():
    return User.objects


@pytest.fixture
def sample_user_data():
    """Sample data for creating user."""
    return {
        "email": "user@example.com",
        "password": "Password123",
    }


@pytest.fixture
def sample_console_user(custom_user_manager, sample_user_data):
    """Simple user instance for create user by user manager."""

    return custom_user_manager.create_user(**sample_user_data)


@pytest.fixture
def sample_console_superuser(custom_user_manager, sample_user_data):
    """Simple superuser instance for create user by user manager."""

    return custom_user_manager.create_superuser(**sample_user_data)


@pytest.fixture
def sample_admin_form_user_data():
    """Simple user data for create user by admin form."""
    return {
        "first_name": "John",
        "email": "john@example.com",
        "password1": "StrongPassword123",
        "password2": "StrongPassword123",
    }


@pytest.fixture
def admin_form_user_data_updated():
    """User data for update user by admin form."""
    return {
        "first_name": "Updated Name",
        "last_name": "Updated Last Name",
        "username": "john_hunter",
        "email": "john@example.com",
        "bio": "Updated Bio",
        "instagram": "updated_instagram",
        "telegram": "updated_telegram",
        "facebook": "updated_facebook",
    }


@pytest.fixture
def sample_user_data_with_username():
    """Sample data with username for creating user."""
    return {
        "email": "user2@example.com",
        "username": "user_name",
        "password": "Password123",
    }


@pytest.fixture
def sample_user_data_not_unique_username():
    """Sample data with not unique username."""
    return {
        "email": "user2@example.com",
        "username": "user_name",
        "password": "Password123",
    }


@pytest.fixture
def sample_superuser_data():
    """Sample data for creating a superuser."""
    return {
        "email": "admin@example.com",
        "password": "Superpassword123",
        "is_staff": True,
        "is_superuser": True,
    }


@pytest.fixture
def full_create_user_data():
    return {
        "email": "testuser@example.com",
        "username": "testuser",
        "first_name": "John",
        "last_name": "Doe",
        "bio": "Test bio",
        "instagram": "test_instagram",
        "telegram": "test_telegram",
        "facebook": "test_facebook",
        "password": "TestPassword123",
    }


@pytest.fixture
def full_create_user_data_without_email(full_create_user_data):
    full_create_user_data.pop("email")
    return full_create_user_data


@pytest.fixture
def full_update_user_data():
    return {
        "email": "updateduser@example.com",
        "username": "updateduser",
        "first_name": "Upjon",
        "last_name": "Updoe",
        "bio": "Updated bio",
        "instagram": "updated_instagram",
        "telegram": "updated_telegram",
        "facebook": "updated_facebook",
        "password": "updatedPassword123",
    }


@pytest.fixture
def user_instance(full_create_user_data):
    return User.objects.create_user(**full_create_user_data)


@pytest.fixture
def superuser_instance(sample_superuser_data):
    return User.objects.create_superuser(**sample_superuser_data)


@pytest.fixture
def user_owner_instance(sample_user_data_with_username):
    return User.objects.create_user(**sample_user_data_with_username)


@pytest.fixture
def user_request(user_instance):
    request = Request(HttpRequest())
    request.user = user_instance
    return request


@pytest.fixture
def owner_request(user_owner_instance):
    request = Request(HttpRequest())
    request.user = user_owner_instance
    return request


@pytest.fixture
def superuser_request(superuser_instance):
    request = Request(HttpRequest())
    request.user = superuser_instance
    return request


@pytest.fixture
def anonim_request():
    request = Request(HttpRequest())
    request.user = AnonymousUser()
    return request


@pytest.fixture
def simple_view():
    return ViewSet()


@pytest.fixture
def user_token(client, full_create_user_data, user_instance):
    auth_data = {
        "email": full_create_user_data["email"],
        "password": full_create_user_data["password"],
    }
    response = client.post(URL_CREATE_TOKEN, data=auth_data)
    return response.data


@pytest.fixture
def token_user(user_instance):
    token = AccessToken.for_user(user_instance)
    return {"access": str(token)}


@pytest.fixture
def user_client(token_user):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token_user['access']}")
    return client


@pytest.fixture
def token_user_owner(user_owner_instance):
    token = AccessToken.for_user(user_owner_instance)
    return {"access": str(token)}


@pytest.fixture
def user_owner_client(token_user_owner):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token_user_owner['access']}")
    return client
