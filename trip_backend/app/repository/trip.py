from datetime import date

from sqlalchemy import and_, select
from sqlalchemy.orm import joinedload

from app.core.database import async_session_maker
from app.models.trip import Trip
from app.repository.base import BaseRepository


class TripRepository(BaseRepository):
    model = Trip

    @classmethod
    async def find_by_id(self, model_id: int):
        async with async_session_maker() as session:
            query = (
                select(self.model)
                .options(joinedload(Trip.marker), joinedload(Trip.user))
                .filter_by(id=model_id)
            )
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_active_trip_by_user(self, user_id: int, start_date: date, end_date: date):
        """Find any active trip the user is currently in during the given time range."""

        async with async_session_maker() as session:
            query = (
                select(self.model)
                .filter_by(user_id=user_id)
                .filter(and_(start_date < Trip.end_date, end_date > Trip.start_date))
            )
            result = await session.execute(query)
            return result.scalar_one_or_none()
