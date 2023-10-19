import pytest

from users.models import User


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
def full_create_user_data_without_email():
    return {
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
def user_instance(full_create_user_data):
    return User.objects.create(**full_create_user_data)
