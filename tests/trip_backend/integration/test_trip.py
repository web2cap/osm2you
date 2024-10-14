import pytest
from app.models.trip import Trip
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_trip_by_id(ac: AsyncClient, create_simple_trip: Trip):
    trip = create_simple_trip
    response = await ac.get(f"/v1/trip/{trip.id}")

    assert response.status_code == 200
    data = response.json()

    assert data["id"] == trip.id
    assert data["description"] == trip.description
    assert data["create_date"] == str(trip.create_date)
    assert data["start_date"] == str(trip.start_date)
    assert data["end_date"] == str(trip.end_date)

    assert data["user"]["id"] == 2
    assert "username" in data["user"] and len(data["user"]["username"])
    assert "first_name" in data["user"]
    assert "last_name" in data["user"]

    assert data["marker"]["id"] == trip.marker_id
    assert "name" in data["marker"]
    assert "location" in data["marker"] and isinstance(data["marker"]["location"], list)
