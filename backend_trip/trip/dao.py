from dao.base import BaseDAO
from trip.models import Trip


class UsersDAO(BaseDAO):
    model = Trip
