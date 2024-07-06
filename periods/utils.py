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

# TODO: Docs
def get_datetime(point_in_time: str,
                 force_datetime: bool = False) -> time | date | datetime:
    if isinstance(point_in_time, time) or isinstance(point_in_time, date) or isinstance(point_in_time, datetime):
        return point_in_time
    else:
        for time_p, date_p, dt_p in zip_longest(TIME_PATTERNS, DATE_PATTERNS, DATETIME_PATTERNS):
            _dt = (_test_pattern(point_in_time, time_p)
                   or _test_pattern(point_in_time, date_p)
                   or _test_pattern(point_in_time, dt_p))
            if not _dt:
                continue
            if not force_datetime:
                if _dt.year == 1900 and _dt.month == 1 and _dt.day == 1:
                    return _dt.timetz()
                elif _dt.hour == 0 and _dt.minute == 0 and _dt.second == 0 and _dt.tzinfo is None:
                    return _dt.date()
            return _dt
        raise ValueError(f"Failed to obtain a datetime object from provided string '{point_in_time}'")

# TODO: Docs
def _test_pattern(string, pattern):
    try:
        return datetime.strptime(string, pattern)
    except (ValueError, TypeError):
        return None
