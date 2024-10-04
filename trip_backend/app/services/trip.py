from datetime import date

from app.core.exceptions import (
    MarkerNotFoundException,
    TripConflictException,
    TripDeleteException,
    TripNotAuthorException,
    TripNotFoundException,
)
from app.models.trip import Trip
from app.models.user import User
from app.repository.marker import MarkerRepository
from app.repository.trip import TripRepository
from app.schema.marker import SMarker
from app.schema.trip import STripCreate, STripDetailed, STripValidateDates
from app.schema.user import SUser


class TripService:
    async def get_trip_with_details(self, trip_id: int) -> STripDetailed:
        trip = await self._get_trip_instance(trip_id)
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
        self._except_if_active_user_trip_exists(
            current_user, trip_data.start_date, trip_data.end_date
        )

        trip_data.user_id = current_user.id
        trip = await TripRepository.insert_data(**dict(trip_data))

        return await self.get_trip_with_details(trip.id)

    async def update_trip_dates(
        self, trip_id: int, trip_data: STripValidateDates, current_user: User
    ) -> STripDetailed:
        trip = await self._get_trip_instance(trip_id)

        self._except_if_active_user_trip_exists(
            current_user, trip_data.start_date, trip_data.end_date
        )
        self._except_if_user_not_author(trip, current_user)

        trip = await TripRepository.update_data(trip_id, **dict(trip_data))

        return await self.get_trip_with_details(trip.id)

    async def delete_trip(self, trip_id: int, current_user: User) -> STripDetailed:
        trip = await self.get_trip_with_details(trip_id)

        self._except_if_user_not_author(trip, current_user)
        if not await TripRepository.delete_by_id(trip_id):
            raise TripDeleteException()

        return trip

    async def _get_trip_instance(self, trip_id: int) -> Trip:
        trip = await TripRepository.find_by_id(trip_id)
        if not trip:
            raise TripNotFoundException()
        return trip

    async def _except_if_active_user_trip_exists(
        self, current_user: User, start_date: date, end_date: date
    ) -> None:
        active_trip = await TripRepository.find_active_trip_by_user(
            current_user.id, start_date, end_date
        )
        if active_trip:
            raise TripConflictException()

    async def _except_if_user_not_author(
        self, trip: STripDetailed | Trip, current_user: User
    ) -> None:
        if trip.user.id != current_user.id:
            raise TripNotAuthorException()
