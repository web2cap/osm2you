from fastapi import HTTPException, status


class AppDefaultHTTPExeption(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


# USER


class InvalidTokenException(AppDefaultHTTPExeption):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Invalid token"


class TokenVerificationFailedException(AppDefaultHTTPExeption):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Token verification failed"


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


class InvalidEndDateException(AppDefaultHTTPExeption):
    status_code = status.HTTP_409_CONFLICT
    detail = "The end date is before today"


class InvalidStartDateException(AppDefaultHTTPExeption):
    status_code = status.HTTP_409_CONFLICT
    detail = "Start date cannot be after end date"


# MARKER
class MarkerNotFoundException(AppDefaultHTTPExeption):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Marker does not exist"
