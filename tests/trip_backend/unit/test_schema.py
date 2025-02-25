from datetime import date, timedelta

import pytest
from pydantic import ValidationError

from app.core.exceptions import InvalidEndDateException, InvalidStartDateException
from app.schema.trip import STripCreate, STripValidateDates


def test_validate_dates_valid():
    """Test date validation with valid dates."""
    today = date.today()
    start_date = today + timedelta(days=1)
    end_date = today + timedelta(days=5)

    trip_dates = STripValidateDates(start_date=start_date, end_date=end_date)

    assert trip_dates.start_date == start_date
    assert trip_dates.end_date == end_date


def test_validate_dates_end_before_today():
    """Test date validation with end date before today."""
    today = date.today()
    start_date = today - timedelta(days=5)
    end_date = today - timedelta(days=1)

    with pytest.raises(InvalidEndDateException):
        STripValidateDates(start_date=start_date, end_date=end_date)


def test_validate_dates_end_before_start():
    """Test date validation with end date before start date."""
    today = date.today()
    start_date = today + timedelta(days=5)
    end_date = today + timedelta(days=2)

    with pytest.raises(InvalidStartDateException):
        STripValidateDates(start_date=start_date, end_date=end_date)


def test_trip_create_with_valid_data():
    """Test creating a trip with valid data."""
    today = date.today()
    data = {
        "start_date": today + timedelta(days=1),
        "end_date": today + timedelta(days=5),
        "description": "Test trip creation",
        "marker_id": 1,
        "user_id": 2,
    }

    trip = STripCreate(**data)

    assert trip.start_date == data["start_date"]
    assert trip.end_date == data["end_date"]
    assert trip.description == data["description"]
    assert trip.marker_id == data["marker_id"]
    assert trip.user_id == data["user_id"]


def test_trip_create_with_missing_required_fields():
    """Test creating a trip with missing marker_id."""
    today = date.today()
    data = {
        "start_date": today + timedelta(days=1),
        "end_date": today + timedelta(days=5),
    }

    with pytest.raises(ValidationError):
        STripCreate(**data)


def test_trip_create_with_str_dates():
    """Test creating a trip with date strings."""
    tomorrow = (date.today() + timedelta(days=1)).isoformat()
    next_week = (date.today() + timedelta(days=7)).isoformat()

    data = {
        "start_date": tomorrow,
        "end_date": next_week,
        "description": "String dates trip",
        "marker_id": 1,
    }

    trip = STripCreate(**data)

    assert isinstance(trip.start_date, date)
    assert isinstance(trip.end_date, date)
