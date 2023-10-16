import pytest

from users.models import User


@pytest.fixture
def custom_user_manager():
    return User.objects


@pytest.fixture
def sample_user(custom_user_manager):
    email = "user@example.com"
    password = "Password123"
    return custom_user_manager.create_user(email, password)


@pytest.fixture
def sample_superuser(custom_user_manager):
    email = "admin@example.com"
    password = "Superpassword123"
    return custom_user_manager.create_superuser(email, password)
