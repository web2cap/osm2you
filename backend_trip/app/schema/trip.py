from datetime import date

from pydantic import BaseModel, field_validator

from app.core.exceptions import InvalidEndDateException, InvalidStartDateException
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

    class Config:
        from_attributes = True


class STripCreate(BaseModel):
    marker_id: int
    start_date: date
    end_date: date
    description: str | None = None
    user_id: date | None = None

    @field_validator("end_date")
    @classmethod
    def validate_end_date(cls, v, values):
        if v < date.today():
            raise InvalidEndDateException()
        return v

    @field_validator("start_date")
    @classmethod
    def validate_start_date(cls, v, values):
        end_date = values.get("end_date")
        if end_date and v > end_date:
            raise InvalidStartDateException()
        return v
