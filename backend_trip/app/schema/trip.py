from datetime import date

from pydantic import BaseModel

from app.schema.marker import SMarker
from app.schema.user import SUser


class STripDetailed(BaseModel):
    id: int
    create_date: date
    start_date: date
    end_date: date
    description: str
    marker: SMarker
    user: SUser
