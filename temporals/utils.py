from datetime import time, date, datetime
from itertools import zip_longest

TIME_PATTERNS = [
    "%I:%M%p",  # 01:51AM
    "%I:%M %p",  # 01:51 AM
    "%I:%M:%S%p",  # 01:51:40AM
    "%I:%M:%S.%f%p",  # 01:51:40.000001AM
    "%I:%M:%S.%f %p",  # 01:51:40.000001 AM
    "%H:%M:%S",  # 13:51:40
    "%H:%M:%S.%f",  # 13:51:40.000001
    "%H:%M",  # 13:51
    "%H:%M%z",  # 13:51-0700 or 13:51-07:00
    "%H:%M %z",  # 13:51 -0700 or 13:51 -07:00
    "%H:%M %z",  # 13:51 GMT/UTC
    "%H:%M:%S %z",  # 13:51:40 -0700 or 13:51:40 -07:00
    "%H:%M:%S.%f %z",  # 13:51:40.000001 -0700 or 13:51:40.000001 -07:00
]

# TODO: Docs on ambiguous patterns - 12/01 (dd/mm) vs 01/12 (mm/dd)
DATE_PATTERNS = [
    "%d/%m/%y",  # 15/12/91
    "%d-%m-%y",  # 15-12-91
    "%y/%m/%d",  # 91/12/15
    "%y-%m-%d",  # 91-12-15
    "%d/%b/%y",  # 15/Jan/91
    "%d-%b-%y",  # 15-Jan-91
    "%y/%b/%d",  # 91/Jan/15
    "%y-%b-%d",  # 91-Jan-15
    "%d/%B/%y",  # 15/January/91
    "%d-%B-%y",  # 15-January-91
    "%y/%B/%d",  # 91/January/15
    "%y-%B-%d",  # 91-January-15
    "%d/%m/%Y",  # 15/12/1991
    "%d-%m-%Y",  # 15-12-1991
    "%Y/%m/%d",  # 1991/12/15
    "%Y-%m-%d",  # 1991-12-15
]

# TODO: Docs on ambiguous patterns - 12/01 (dd/mm) vs 01/12 (mm/dd)
DATETIME_PATTERNS = [
    "%Y-%m-%dT%H:%M",  # 1991-12-15T13:51
    "%Y/%m/%dT%H:%M",  # 1991/12/15T13:51
    "%Y-%m-%dT%H:%M%z",  # 1991-12-15T13:51-0700 or 1991-12-15T13:51-07:00
    "%Y/%m/%dT%H:%M%z",  # 1991/12/15T13:51-0700 or 1991/12/15T13:51-07:00
    "%Y-%m-%d %H:%M",  # 1991-12-15 13:51
    "%/-%m/%d %H:%M",  # 1991/12/15 13:51
    "%Y-%m-%d %H:%M%z",  # 1991-12-15 13:51-0700 or 1991-12-15 13:51-07:00
    "%Y/%m/%d %H:%M%z",  # 1991/12/15 13:51-0700 or 1991/12/15 13:51-07:00
    "%Y-%m-%dT%H:%M:%S",  # 1991-12-15T13:51:40
    "%Y-%m-%dT%H:%M:%S.%f",  # 1991-12-15T13:51:40.000001
    "%Y/%m/%dT%H:%M:%S",  # 1991/12/15T13:51:40
    "%Y/%m/%dT%H:%M:%S.%f",  # 1991/12/15T13:51:40.000001
    "%Y-%m-%d %H:%M:%S",  # 1991-12-15 13:51:40
    "%Y-%m-%d %H:%M:%S.%f",  # 1991-12-15 13:51:40.000001
    "%Y/%m/%d %H:%M:%S",  # 1991/12/15 13:51:40
    "%Y/%m/%d %H:%M:%S.%f",  # 1991/12/15 13:51:40.000001
    "%Y-%m-%dT%H:%M:%S%z",  # 1991-12-15T13:51:40-0700 or 1991-12-15T13:51:40-07:00
    "%Y/%m/%dT%H:%M:%S%z",  # 1991/12/15T13:51:40-0700 or 1991/12/15T13:51:40-07:00
    "%Y-%m-%dT%H:%M:%S%Z",  # 1991-12-15T13:51:40GMT/UTC
    "%Y-%m-%d %H:%M:%S %Z",  # 1991-12-15T13:51:40 GMT/UTC
    "%Y-%m-%dT%H:%M%Z",  # 1991-12-15T13:51GMT/UTC
    "%Y-%m-%d %H:%M%Z",  # 1991-12-15 13:51GMT/UTC
]


def get_datetime(point_in_time: str,
                 force_datetime: bool = False) -> time | date | datetime:
    """
    A helper function used by the PeriodFactory object when either the start or the end of a period is a string.
    The goal of this function is to best determine what type the provided string fits (time, date, datetime) and return
    that so the PeriodFactory constructor that initialize the correct Period type.

    Via the _test_defaults function, this function will test if the string can be initialized by using one of the
    standard from<something> methods that time, date and datetime objects have; if that fails, it will fall back on
    trying to bruteforce the string into an object by iterating over the saved patterns lists.

    Args:
        point_in_time: The string that has to be initialized;
        force_datetime: If True, the method will always a return a datetime object, even if the string is determined to
            be a time or a date.

    Returns:
        time | date | datetime

    Raises:
        ValueError: The function has failed to initialize the string.
    """
    # Check if the provided object is already an instance
    if isinstance(point_in_time, time) or isinstance(point_in_time, date) or isinstance(point_in_time, datetime):
        if force_datetime:
            point_in_time = convert_to_datetime(point_in_time)
        return point_in_time

    # Try the default datetime constructors
    _dt = _test_defaults(point_in_time)
    if _dt:
        """
        If 'force_datetime' is True and _dt isn't an instance of datetime already, turn it into one by imitating the
        behaviour of datetime's strptime() method - if a time, set date to 1900-01-01; if a date, set time to 0:0.
        """
        if force_datetime and not isinstance(_dt, datetime):
            _dt = convert_to_datetime(_dt)
        return _dt

    # Fall back on the known patterns
    for time_p, date_p, dt_p in zip_longest(TIME_PATTERNS, DATE_PATTERNS, DATETIME_PATTERNS):
        _dt = (_test_pattern(point_in_time, time_p)
               or _test_pattern(point_in_time, date_p)
               or _test_pattern(point_in_time, dt_p))
        if not _dt:
            continue
        """
        Opposite of what's happening above - if the 'force_datetime' bool is set to False, return only the time or the
        date object. Evaluation is done based on:
            For date objects, the hour, minute and second must be 0, and there must be no timezone information;
            For time objects, the year must be 1900, month and day must be 1.
        """
        if not force_datetime:
            if _dt.year == 1900 and _dt.month == 1 and _dt.day == 1:
                return _dt.timetz()
            elif _dt.hour == 0 and _dt.minute == 0 and _dt.second == 0 and _dt.tzinfo is None:
                return _dt.date()
        return _dt
    raise ValueError(f"Failed to obtain a datetime object from provided string '{point_in_time}'")


def _test_pattern(point_in_time: str,
                  pattern: str) -> datetime | None:
    """
    Helper method used by the `get_datetime` function above to try and initialize the point_in_time string as a datetime
    object by using the provided `pattern` parameter.

    Args:
        point_in_time: String to test the format against;
        pattern: The datetime.strptime pattern to use;

    Returns:
        Either the created datetime object or None
    """
    try:
        return datetime.strptime(point_in_time, pattern)
    except (ValueError, TypeError):
        return None


def _test_defaults(point_in_time: str | int | float) -> time | date | datetime | None:
    """
    Layer to invoke the different datetime constructor functions below.

    Args:
        point_in_time: The object that will be used by the constructors to create an instance of time, date or datetime

    Returns:
        time | date | datetime | None
    """
    resolved_pit = (_test_time(point_in_time)
                    or _test_date(point_in_time)
                    or _test_datetime(point_in_time))
    return resolved_pit


def _test_time(point_in_time: str) -> time | None:
    """ Try to create a datetime.time object """
    try:
        return time.fromisoformat(point_in_time)
    except (ValueError, TypeError):
        return None


def _test_date(point_in_time: str | int) -> date | None:
    """ Try to create a datetime.date object """
    pit_str: str = _convert_to_type(point_in_time, str)
    pit_int: int = _convert_to_type(point_in_time, int)
    try:
        return date.fromisoformat(pit_str)
    except (ValueError, TypeError):
        pass
    try:
        return date.fromordinal(pit_int)
    except (ValueError, TypeError):
        pass
    return None


def _test_datetime(point_in_time: str | float) -> datetime | None:
    """ Try to create a datetime.date object """
    pit_str: str = _convert_to_type(point_in_time, str)
    pit_float: float = _convert_to_type(point_in_time, float)
    try:
        return datetime.fromisoformat(pit_str)
    except (ValueError, TypeError):
        pass
    try:
        return datetime.fromtimestamp(pit_float)
    except (ValueError, TypeError):
        pass
    return None


def _convert_to_type(value, target_type):
    try:
        return target_type(value)
    except (ValueError, TypeError):
        return None


def convert_to_datetime(value: time | date) -> datetime:
    if isinstance(value, datetime):
        return value
    if isinstance(value, date):
        _dt = datetime.combine(value, time(0, 0, 0))
    else:
        _dt = datetime.combine(date(1900, 1, 1), value, tzinfo=value.tzinfo)
    return _dt
