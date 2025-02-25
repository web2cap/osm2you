from datetime import date, timedelta

import pytest

from app.core.exceptions import (
    MarkerNotFoundException,
    TripConflictException,
    TripNotFoundException,
)
from app.schema.trip import STripCreate


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


@pytest.mark.asyncio
async def test_add_trip(trip_service, current_user):
    """Test adding a new trip."""
    trip_data = STripCreate(
        start_date=date.today() + timedelta(days=5),
        end_date=date.today() + timedelta(days=10),
        description="Service test trip",
        marker_id=1,
    )

    result = await trip_service.add_trip(trip_data, current_user)

    assert result.description == "Service test trip"
    assert result.marker.id == 1
    assert result.user.id == 2


@pytest.mark.asyncio
async def test_add_trip_marker_not_found(trip_service, current_user):
    """Test adding a trip with a non-existent marker."""
    trip_data = STripCreate(
        start_date=date.today() + timedelta(days=5),
        end_date=date.today() + timedelta(days=10),
        description="Invalid marker trip",
        marker_id=9999,
    )

    with pytest.raises(MarkerNotFoundException):
        await trip_service.add_trip(trip_data, current_user)


@pytest.mark.asyncio
async def test_add_trip_conflict(trip_service, current_user, create_simple_trip):
    """Test adding a trip that conflicts with an existing trip."""
    trip_data = STripCreate(
        start_date=create_simple_trip.start_date,
        end_date=create_simple_trip.end_date,
        description="Overlapping trip",
        marker_id=1,
    )

    with pytest.raises(TripConflictException):
        await trip_service.add_trip(trip_data, current_user)
