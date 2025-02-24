import pytest

from app.repository.trip import TripRepository


@pytest.mark.asyncio
async def test_find_by_id(create_simple_trip):
    """Test finding a trip by ID."""
    trip_id = create_simple_trip.id

    trip = await TripRepository.find_by_id(trip_id)

    assert trip is not None
    assert trip.id == trip_id
    assert trip.description == "Test trip"
    assert trip.marker is not None
    assert trip.user is not None


@pytest.mark.asyncio
async def test_find_by_id_not_found():
    """Test finding a non-existent trip by ID."""
    trip = await TripRepository.find_by_id(9999)

    assert trip is None
