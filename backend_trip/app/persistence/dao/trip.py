from app.domain.models.trip import Trip
from app.persistence.dao.base import BaseDAO


class TripDAO(BaseDAO):
    model = Trip
