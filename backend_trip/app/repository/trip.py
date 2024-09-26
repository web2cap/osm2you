from app.models.trip import Trip
from app.repository.base import BaseRepository


class TripRepository(BaseRepository):
    model = Trip
