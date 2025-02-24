import pytest

from app.core.exceptions import TripNotFoundException
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


@pytest.mark.asyncio
async def test_get_trip_with_details(trip_service, create_simple_trip):
    """Test retrieving trip details."""
    trip_id = create_simple_trip.id

    result = await trip_service.get_trip_with_details(trip_id)

    assert result.id == trip_id
    assert result.description == "Test trip"
    assert isinstance(result.marker, object)
    assert result.marker.id == 1
    assert result.user.id == 2


@pytest.mark.asyncio
async def test_get_trip_not_found(trip_service):
    """Test retrieving a non-existent trip."""
    with pytest.raises(TripNotFoundException):
        await trip_service.get_trip_with_details(9999)
