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


class STripValidateDates(BaseModel):
    start_date: date
    end_date: date

    @field_validator("end_date")
    @classmethod
    def validate_end_date(cls, v, info):
        if v < date.today():
            raise InvalidEndDateException()
        return v

    @field_validator("start_date")
    @classmethod
    def validate_start_date(cls, v, info):
        end_date = info.data.get("end_date")
        if end_date and v > end_date:
            raise InvalidStartDateException()
        return v


class STripCreate(STripValidateDates):
    marker_id: int
    start_date: date
    end_date: date
    description: str | None = None
    user_id: int | None = None
