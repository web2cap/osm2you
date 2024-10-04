from app.core.exceptions import (
    MarkerNotFoundException,
    TripConflictException,
    TripDeleteException,
    TripNotAuthorException,
    TripNotFoundException,
)
from app.models.user import User
from app.repository.marker import MarkerRepository
from app.repository.trip import TripRepository
from app.schema.marker import SMarker
from app.schema.trip import STripCreate, STripDetailed
from app.schema.user import SUser


class TripService:
    async def get_trip_with_details(self, trip_id: int) -> STripDetailed:
        trip = await TripRepository.find_by_id(trip_id)
        if not trip:
            raise TripNotFoundException
        return STripDetailed(
            id=trip.id,
            create_date=trip.create_date,
            start_date=trip.start_date,
            end_date=trip.end_date,
            description=trip.description,
            marker=SMarker.from_orm_marker(trip.marker),
            user=SUser(
                id=trip.user.id,
                username=trip.user.username,
                first_name=trip.user.first_name,
                last_name=trip.user.last_name,
            ),
        )

    async def add_trip(self, trip_data: STripCreate, current_user: User) -> STripDetailed:
        """Add trip service.
        Validation:
         - check if marker exists
         - check if user is already on another trip
        """

        if not await MarkerRepository.find_by_id(trip_data.marker_id):
            raise MarkerNotFoundException()

        active_trip = await TripRepository.find_active_trip_by_user(
            current_user.id, trip_data.start_date, trip_data.end_date
        )
        if active_trip:
            raise TripConflictException()

        trip_data.user_id = current_user.id
        trip = await TripRepository.insert_data(**dict(trip_data))

        return await self.get_trip_with_details(trip.id)

    async def delete_trip(self, trip_id: int, current_user: User) -> STripDetailed:
        trip = await self.get_trip_with_details(trip_id)

        if trip.user.id != current_user.id:
            raise TripNotAuthorException()

        if not await TripRepository.delete_by_id(trip_id):
            raise TripDeleteException()

        return trip
