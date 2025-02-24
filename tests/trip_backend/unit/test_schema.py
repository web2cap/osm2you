from datetime import date, timedelta

import pytest

from app.core.exceptions import InvalidEndDateException, InvalidStartDateException
from app.schema.trip import STripValidateDates


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
