from datetime import date, timedelta

import pytest
from app.repository.trip import TripRepository
from app.schema.trip import STripCreate


@pytest.fixture
async def trip_data_marker1_user2():
    return STripCreate(
        start_date=date.today() - timedelta(days=1),
        end_date=date.today() + timedelta(days=1),
        description="Test trip",
        marker_id=1,
        user_id=2,
    )


@pytest.fixture
async def create_simple_trip(trip_data_marker1_user2):
    return await TripRepository.insert_data(**dict(trip_data_marker1_user2))
