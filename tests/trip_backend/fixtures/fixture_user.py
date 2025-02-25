import pytest

from app.models.user import User


@pytest.fixture
def current_user():
    return User(
        id=2, username="testuser", first_name="Test", last_name="User", is_active=True
    )
