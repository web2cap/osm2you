from datetime import timedelta

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


@pytest.mark.asyncio
async def test_find_all(session, create_simple_trip):
    """Test finding all trips."""
    trips = await TripRepository.find_all()

    assert len(trips) >= 1
    assert any(trip.id == create_simple_trip.id for trip in trips)


@pytest.mark.asyncio
async def test_find_active_trip_by_user(create_simple_trip):
    """Test finding active trips for a user."""
    # Check for overlap with existing trip
    start_date = create_simple_trip.start_date - timedelta(days=1)
    end_date = create_simple_trip.end_date + timedelta(days=1)

    trip = await TripRepository.find_active_trip_by_user(
        create_simple_trip.user_id, start_date, end_date
    )

    assert trip is not None
    assert trip.id == create_simple_trip.id


@pytest.mark.asyncio
async def test_find_active_trip_by_user_no_overlap(create_simple_trip):
    """Test finding active trips when there's no overlap."""
    # Dates that don't overlap with existing trip
    start_date = create_simple_trip.end_date + timedelta(days=1)
    end_date = start_date + timedelta(days=5)

    trip = await TripRepository.find_active_trip_by_user(
        create_simple_trip.user_id, start_date, end_date
    )

    assert trip is None
