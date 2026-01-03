"""
DateTime utilities for common date and time operations.
"""

from datetime import datetime, date, timedelta
from typing import Optional, List, Union
import time


def now() -> datetime:
    """Get the current datetime."""
    return datetime.now()


def now_timestamp() -> float:
    """Get the current timestamp as a float."""
    return time.time()


def now_timestamp_ms() -> int:
    """Get the current timestamp in milliseconds."""
    return int(time.time() * 1000)


def today() -> date:
    """Get today's date."""
    return date.today()


def parse_date(
    date_string: str,
    fmt: str = "%Y-%m-%d",
) -> date:
    """
    Parse a date string into a date object.

    Args:
        date_string: The date string to parse
        fmt: The format of the date string (default: "%Y-%m-%d")

    Returns:
        A date object
    """
    return datetime.strptime(date_string, fmt).date()


def parse_datetime(
    datetime_string: str,
    fmt: str = "%Y-%m-%d %H:%M:%S",
) -> datetime:
    """
    Parse a datetime string into a datetime object.

    Args:
        datetime_string: The datetime string to parse
        fmt: The format of the datetime string (default: "%Y-%m-%d %H:%M:%S")

    Returns:
        A datetime object
    """
    return datetime.strptime(datetime_string, fmt)


def format_date(d: date, fmt: str = "%Y-%m-%d") -> str:
    """
    Format a date object into a string.

    Args:
        d: The date object to format
        fmt: The output format (default: "%Y-%m-%d")

    Returns:
        A formatted date string
    """
    return d.strftime(fmt)


def format_datetime(dt: datetime, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Format a datetime object into a string.

    Args:
        dt: The datetime object to format
        fmt: The output format (default: "%Y-%m-%d %H:%M:%S")

    Returns:
        A formatted datetime string
    """
    return dt.strftime(fmt)


def date_range(
    start: Union[str, date],
    end: Union[str, date],
    fmt: str = "%Y-%m-%d",
) -> List[date]:
    """
    Generate a list of dates between start and end (inclusive).

    Args:
        start: Start date (string or date object)
        end: End date (string or date object)
        fmt: Format for parsing date strings (default: "%Y-%m-%d")

    Returns:
        A list of date objects
    """
    if isinstance(start, str):
        start = parse_date(start, fmt)
    if isinstance(end, str):
        end = parse_date(end, fmt)

    dates = []
    current = start
    while current <= end:
        dates.append(current)
        current += timedelta(days=1)
    return dates


def days_between(
    date1: Union[str, date],
    date2: Union[str, date],
    fmt: str = "%Y-%m-%d",
) -> int:
    """
    Calculate the number of days between two dates.

    Args:
        date1: First date (string or date object)
        date2: Second date (string or date object)
        fmt: Format for parsing date strings (default: "%Y-%m-%d")

    Returns:
        Number of days between the dates (absolute value)
    """
    if isinstance(date1, str):
        date1 = parse_date(date1, fmt)
    if isinstance(date2, str):
        date2 = parse_date(date2, fmt)

    return abs((date2 - date1).days)


def add_days(d: Union[str, date], days: int, fmt: str = "%Y-%m-%d") -> date:
    """
    Add days to a date.

    Args:
        d: The date (string or date object)
        days: Number of days to add (can be negative)
        fmt: Format for parsing date strings (default: "%Y-%m-%d")

    Returns:
        A new date object
    """
    if isinstance(d, str):
        d = parse_date(d, fmt)
    return d + timedelta(days=days)


def start_of_day(dt: Optional[datetime] = None) -> datetime:
    """
    Get the start of the day (midnight) for a given datetime.

    Args:
        dt: The datetime (default: current datetime)

    Returns:
        A datetime object set to midnight
    """
    if dt is None:
        dt = now()
    return dt.replace(hour=0, minute=0, second=0, microsecond=0)


def end_of_day(dt: Optional[datetime] = None) -> datetime:
    """
    Get the end of the day (23:59:59.999999) for a given datetime.

    Args:
        dt: The datetime (default: current datetime)

    Returns:
        A datetime object set to end of day
    """
    if dt is None:
        dt = now()
    return dt.replace(hour=23, minute=59, second=59, microsecond=999999)


def is_weekend(d: Union[str, date, None] = None, fmt: str = "%Y-%m-%d") -> bool:
    """
    Check if a date is a weekend (Saturday or Sunday).

    Args:
        d: The date to check (default: today)
        fmt: Format for parsing date strings (default: "%Y-%m-%d")

    Returns:
        True if weekend, False otherwise
    """
    if d is None:
        d = today()
    elif isinstance(d, str):
        d = parse_date(d, fmt)
    return d.weekday() >= 5


def timestamp_to_datetime(ts: Union[int, float]) -> datetime:
    """
    Convert a Unix timestamp to a datetime object.

    Args:
        ts: Unix timestamp (seconds since epoch)

    Returns:
        A datetime object
    """
    return datetime.fromtimestamp(ts)


def datetime_to_timestamp(dt: datetime) -> float:
    """
    Convert a datetime object to a Unix timestamp.

    Args:
        dt: A datetime object

    Returns:
        Unix timestamp as a float
    """
    return dt.timestamp()
