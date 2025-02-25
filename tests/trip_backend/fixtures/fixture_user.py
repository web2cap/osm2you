import pytest

from app.models.user import User


@pytest.fixture
def current_user():
    return User(
        id=2, username="testuser", first_name="Test", last_name="User", is_active=True
    )


@pytest.fixture
def non_owner_user():
    return User(
        id=1, username="otheruser", first_name="Other", last_name="User", is_active=True
    )
