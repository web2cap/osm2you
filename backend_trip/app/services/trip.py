from app.repository.trip import TripRepository
from app.schema.marker import SMarker
from app.schema.trip import STripDetailed
from app.schema.user import SUser


class TripService:
    def __init__(self, trip_repo: TripRepository):
        self.trip_repo = trip_repo

    async def get_trip_with_details(self, trip_id: int) -> STripDetailed:
        trip = await self.trip_repo.find_by_id(trip_id)
        if not trip:
            raise ValueError("Trip not found")
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
