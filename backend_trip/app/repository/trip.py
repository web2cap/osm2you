from typing import Optional, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.models.trip import Trip
from app.repository.base import BaseRepository

T = TypeVar("T")


class TripRepository(BaseRepository[Trip]):
    model = Trip

    async def find_by_id(self, model_id: int) -> Optional[T]:
        async with self.session as session:
            query = (
                select(self.model)
                .options(joinedload(Trip.marker), joinedload(Trip.user))
                .filter_by(id=model_id)
            )
            result = await session.execute(query)
            return result.scalar_one_or_none()
