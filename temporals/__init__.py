from datetime import time, date, datetime
from .utils import get_datetime
from .periods import DatePeriod, TimePeriod, DatetimePeriod


__all__ = [
    'PeriodFactory',
    'DatePeriod',
    'TimePeriod',
    'DatetimePeriod',
    'get_datetime',
]


class PeriodFactory:

    # TODO: Docs
    def __new__(cls,
                start,
                end,
                force_datetime: bool = False) -> TimePeriod | DatePeriod | DatetimePeriod:
        start = get_datetime(start, force_datetime)
        end = get_datetime(end, force_datetime)
        if type(start) is time and type(end) is time:
            return TimePeriod(start, end)
        if type(start) is date and type(end) is date:
            return DatePeriod(start, end)
        if type(start) is datetime and type(end) is datetime:
            return DatetimePeriod(start, end)
        raise ValueError(f"Could not find suitable period type for the provided values")
