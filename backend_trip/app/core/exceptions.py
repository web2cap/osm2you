from fastapi import HTTPException, status


class AppDefaultHTTPExeption(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


# TRIP


class TripNotFoundException(AppDefaultHTTPExeption):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Trip does not exist"


class TripConflictException(AppDefaultHTTPExeption):
    status_code = status.HTTP_409_CONFLICT
    detail = "You are trying to book overlapping trips"


class UserNotFoundException(AppDefaultHTTPExeption):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "User does not exist"


class MarkerNotFoundException(AppDefaultHTTPExeption):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Marker does not exist"


class InvalidDateException(AppDefaultHTTPExeption):
    status_code = status.HTTP_409_CONFLICT
    detail = "The end date is before today"
