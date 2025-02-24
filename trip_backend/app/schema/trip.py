from datetime import date, datetime

from pydantic import BaseModel, model_validator

from app.core.exceptions import InvalidEndDateException, InvalidStartDateException
from app.schema.marker import SMarker
from app.schema.user import SUser

DATE_FORMAT = "%Y-%m-%d"

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

    @model_validator(mode="before")
    @classmethod
    def validate_dates(cls, values):

        start_date = values.get("start_date")
        end_date = values.get("end_date")

        # Let Pydantic handle missing fields
        if not end_date or not start_date:
            return values  

        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, DATE_FORMAT).date()
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, DATE_FORMAT).date()

        # can't finished before today
        if end_date < date.today():
            raise InvalidEndDateException()

        # can't ends before start
        if end_date < start_date:
            raise InvalidStartDateException()

        return values



class STripCreate(STripValidateDates):
    marker_id: int
    start_date: date
    end_date: date
    description: str | None = None
    user_id: int | None = None
