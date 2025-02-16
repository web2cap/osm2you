from datetime import date, timedelta
import pytest
from app.models.trip import Trip
from app.schema.trip import STripCreate
from httpx import AsyncClient


class TestTrip:
    URL_TRIP = "/v1/trip/"
    
    ### GET
    @pytest.mark.asyncio
    async def test_get_trip_by_id(self, ac: AsyncClient, create_simple_trip: Trip):
        """Test getting a trip successfully."""
        trip = create_simple_trip
        response = await ac.get(f"{self.URL_TRIP}{trip.id}")

        assert response.status_code == 200
        data = response.json()

        assert data["id"] == trip.id
        assert data["description"] == trip.description
        assert data["create_date"] == str(trip.create_date)
        assert data["start_date"] == str(trip.start_date)
        assert data["end_date"] == str(trip.end_date)

        assert data["user"]["id"] == trip.user_id
        assert "username" in data["user"] and len(data["user"]["username"])
        assert "first_name" in data["user"]
        assert "last_name" in data["user"]

        assert data["marker"]["id"] == trip.marker_id
        assert "name" in data["marker"]
        assert "location" in data["marker"] and isinstance(
            data["marker"]["location"], list
        )
    @pytest.mark.asyncio
    async def test_get_trip_by_auth_user(self, authenticated_ac: AsyncClient, create_simple_trip: Trip):
        """Test retrieving a trip by an authenticated user."""
        response = await authenticated_ac.get(f"{self.URL_TRIP}{create_simple_trip.id}")
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_get_trip_not_found(self, ac: AsyncClient, create_simple_trip: Trip):
        """Test retrieving a non-existent trip."""
        response = await ac.get(f"{self.URL_TRIP}9999")
        assert response.status_code == 404

    ### POST
    @pytest.mark.asyncio
    async def test_create_trip_success(self, authenticated_ac: AsyncClient, trip_data_marker1_user2: STripCreate):
        """Test creating a trip successfully."""
        response = await authenticated_ac.post(
            self.URL_TRIP,
            json= {
                "marker_id": trip_data_marker1_user2.marker_id,
                "start_date": str(trip_data_marker1_user2.start_date),
                "end_date": str(trip_data_marker1_user2.end_date),
                "description": trip_data_marker1_user2.description
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["id"]
        assert data["description"] == "Test trip"

    @pytest.mark.asyncio
    async def test_create_trip_end_date_in_past(self, authenticated_ac: AsyncClient, trip_data_marker1_user2: STripCreate):
        """Test creating a trip with invalid dates (end_date in past)."""
        response = await authenticated_ac.post(
            self.URL_TRIP,
            json= {
                "marker_id": trip_data_marker1_user2.marker_id,
                "start_date": str(date.today() - timedelta(days=2)),
                "end_date": str(date.today() - timedelta(days=1)),
                "description": trip_data_marker1_user2.description
            }
        )
        assert response.status_code == 409

    @pytest.mark.asyncio
    async def test_create_trip_end_date_less_start_date(self, authenticated_ac: AsyncClient, trip_data_marker1_user2: STripCreate):
        """Test creating a trip with invalid dates (end_date before start_date)."""
        response = await authenticated_ac.post(
            self.URL_TRIP,
            json= {
                "marker_id": trip_data_marker1_user2.marker_id,
                "start_date": str(date.today() + timedelta(days=2)),
                "end_date": str(date.today() + timedelta(days=1)),
                "description": trip_data_marker1_user2.description
            }
        )
        assert response.status_code == 409

    ## UPDATE
    @pytest.mark.asyncio
    async def test_update_trip_success(self, authenticated_ac: AsyncClient, create_simple_trip: Trip):
        """Test updating trip dates successfully."""

        new_dates={
                "start_date": str(create_simple_trip.start_date + timedelta(days=1)),
                "end_date": str(create_simple_trip.end_date + timedelta(days=10)),
        }

        response = await authenticated_ac.put(
            f"{self.URL_TRIP}{create_simple_trip.id}",
            json=new_dates
        )
        assert response.status_code == 200
        data = response.json()
        assert data["start_date"] == new_dates["start_date"]
        assert data["end_date"] == new_dates["end_date"]
    
    @pytest.mark.asyncio
    async def test_update_trip_end_date_less_start_date(self, authenticated_ac: AsyncClient, create_simple_trip: Trip):
        """Test updating trip with invalid dates (end_date before start_date)."""

        invalid_dates={
                "start_date": str(create_simple_trip.start_date + timedelta(days=10)),
                "end_date": str(create_simple_trip.start_date + timedelta(days=1)),
        }

        response = await authenticated_ac.put(
            f"{self.URL_TRIP}{create_simple_trip.id}",
            json=invalid_dates
        )
        assert response.status_code == 409
    
    @pytest.mark.asyncio
    async def test_update_trip_end_date_in_past(self, authenticated_ac: AsyncClient, create_simple_trip: Trip):
        """Test updating trip with invalid dates (end_date in past)"""

        invalid_dates={
            "start_date": str(date.today() - timedelta(days=2)),
            "end_date": str(date.today() - timedelta(days=1)),
        }

        response = await authenticated_ac.put(
            f"{self.URL_TRIP}{create_simple_trip.id}",
            json=invalid_dates
        )
        assert response.status_code == 409
       
    ### DELETE
    @pytest.mark.asyncio
    async def test_delete_trip_success(self, authenticated_ac: AsyncClient, create_simple_trip: Trip):
        """Test deleting trip successfully."""

        response = await authenticated_ac.delete(f"{self.URL_TRIP}{create_simple_trip.id}")
        assert response.status_code == 204

    @pytest.mark.asyncio
    async def test_delete_trip_not_found(self, authenticated_ac: AsyncClient, create_simple_trip: Trip):
        """Test deleting a non-existent trip."""
        
        response = await authenticated_ac.delete(f"{self.URL_TRIP}9999")
        assert response.status_code == 404