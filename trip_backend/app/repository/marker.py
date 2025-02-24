from app.models.marker import Marker
from app.repository.base import BaseRepository


class MarkerRepository(BaseRepository):
    model = Marker
