from sqlalchemy import select
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
