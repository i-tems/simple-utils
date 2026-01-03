"""Tests for datetime_utils module."""

from datetime import date, datetime, timedelta

import pytest

from simple_utils import datetime_utils


class TestNow:
    def test_now_returns_datetime(self):
        result = datetime_utils.now()
        assert isinstance(result, datetime)

    def test_now_timestamp_returns_float(self):
        result = datetime_utils.now_timestamp()
        assert isinstance(result, float)
        assert result > 0

    def test_now_timestamp_ms_returns_int(self):
        result = datetime_utils.now_timestamp_ms()
        assert isinstance(result, int)
        assert result > 0


class TestToday:
    def test_today_returns_date(self):
        result = datetime_utils.today()
        assert isinstance(result, date)
        assert result == date.today()


class TestParse:
    def test_parse_date_default_format(self):
        result = datetime_utils.parse_date("2024-01-15")
        assert result == date(2024, 1, 15)

    def test_parse_date_custom_format(self):
        result = datetime_utils.parse_date("15/01/2024", "%d/%m/%Y")
        assert result == date(2024, 1, 15)

    def test_parse_datetime_default_format(self):
        result = datetime_utils.parse_datetime("2024-01-15 10:30:00")
        assert result == datetime(2024, 1, 15, 10, 30, 0)

    def test_parse_datetime_custom_format(self):
        result = datetime_utils.parse_datetime("15/01/2024 10:30", "%d/%m/%Y %H:%M")
        assert result == datetime(2024, 1, 15, 10, 30)


class TestFormat:
    def test_format_date_default(self):
        d = date(2024, 1, 15)
        assert datetime_utils.format_date(d) == "2024-01-15"

    def test_format_date_custom(self):
        d = date(2024, 1, 15)
        assert datetime_utils.format_date(d, "%d/%m/%Y") == "15/01/2024"

    def test_format_datetime_default(self):
        dt = datetime(2024, 1, 15, 10, 30, 0)
        assert datetime_utils.format_datetime(dt) == "2024-01-15 10:30:00"

    def test_format_datetime_custom(self):
        dt = datetime(2024, 1, 15, 10, 30)
        assert datetime_utils.format_datetime(dt, "%d/%m/%Y %H:%M") == "15/01/2024 10:30"


class TestDateRange:
    def test_date_range_with_strings(self):
        result = datetime_utils.date_range("2024-01-01", "2024-01-03")
        assert len(result) == 3
        assert result[0] == date(2024, 1, 1)
        assert result[2] == date(2024, 1, 3)

    def test_date_range_with_dates(self):
        start = date(2024, 1, 1)
        end = date(2024, 1, 3)
        result = datetime_utils.date_range(start, end)
        assert len(result) == 3

    def test_date_range_single_day(self):
        result = datetime_utils.date_range("2024-01-01", "2024-01-01")
        assert len(result) == 1


class TestDaysBetween:
    def test_days_between_strings(self):
        result = datetime_utils.days_between("2024-01-01", "2024-01-10")
        assert result == 9

    def test_days_between_reversed(self):
        result = datetime_utils.days_between("2024-01-10", "2024-01-01")
        assert result == 9  # absolute value

    def test_days_between_same_day(self):
        result = datetime_utils.days_between("2024-01-01", "2024-01-01")
        assert result == 0


class TestAddDays:
    def test_add_positive_days(self):
        result = datetime_utils.add_days("2024-01-01", 5)
        assert result == date(2024, 1, 6)

    def test_add_negative_days(self):
        result = datetime_utils.add_days("2024-01-10", -5)
        assert result == date(2024, 1, 5)

    def test_add_days_with_date_object(self):
        d = date(2024, 1, 1)
        result = datetime_utils.add_days(d, 5)
        assert result == date(2024, 1, 6)


class TestStartEndOfDay:
    def test_start_of_day(self):
        dt = datetime(2024, 1, 15, 14, 30, 45)
        result = datetime_utils.start_of_day(dt)
        assert result == datetime(2024, 1, 15, 0, 0, 0, 0)

    def test_start_of_day_none(self):
        result = datetime_utils.start_of_day()
        assert result.hour == 0
        assert result.minute == 0
        assert result.second == 0

    def test_end_of_day(self):
        dt = datetime(2024, 1, 15, 14, 30, 45)
        result = datetime_utils.end_of_day(dt)
        assert result.hour == 23
        assert result.minute == 59
        assert result.second == 59


class TestIsWeekend:
    def test_saturday_is_weekend(self):
        assert datetime_utils.is_weekend("2024-01-06") is True  # Saturday

    def test_sunday_is_weekend(self):
        assert datetime_utils.is_weekend("2024-01-07") is True  # Sunday

    def test_monday_is_not_weekend(self):
        assert datetime_utils.is_weekend("2024-01-08") is False  # Monday

    def test_friday_is_not_weekend(self):
        assert datetime_utils.is_weekend("2024-01-05") is False  # Friday


class TestTimestamp:
    def test_timestamp_to_datetime(self):
        ts = 1705312800  # 2024-01-15 10:00:00 UTC
        result = datetime_utils.timestamp_to_datetime(ts)
        assert isinstance(result, datetime)

    def test_datetime_to_timestamp(self):
        dt = datetime(2024, 1, 15, 10, 0, 0)
        result = datetime_utils.datetime_to_timestamp(dt)
        assert isinstance(result, float)

    def test_roundtrip(self):
        original = datetime(2024, 1, 15, 10, 0, 0)
        ts = datetime_utils.datetime_to_timestamp(original)
        result = datetime_utils.timestamp_to_datetime(ts)
        assert result == original
