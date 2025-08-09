from temporals.interfaces import AbstractDuration
from .utils import verify_type


class Duration(AbstractDuration):
    """ Implementation of the AbstractDuration interface with a precision down to the second - in order to avoid
    ambiguity with float numbers (is the decimal value a millisecond/microsecond/nanosecond?), this is the Duration
    implemented by all Periods that come as part of this library.
    """

    def __init__(self, total_seconds: int, years: int, months: int, days: int, hours: int, minutes: int, seconds: int):
        self._total: int = verify_type('total_seconds', int, total_seconds)
        self._years: int = verify_type('years', int, years)
        self._months: int = verify_type('months', int, months)
        self._days: int = verify_type('days', int, days)
        self._hours: int = verify_type('hours', int, hours)
        self._minutes: int = verify_type('minutes', int, minutes)
        self._seconds: int = verify_type('seconds', int, seconds)

    def __str__(self):
        return self.isoformat(fold=False)

    def __repr__(self):
        return (f"Duration(total_seconds={self._total}, years={self._years}, months={self._months}, days={self._days}, "
                f"hours={self._hours}, minutes={self._minutes}, seconds={self._seconds})")

    @classmethod
    def from_seconds(cls, seconds: int):
        verify_type('seconds', int, seconds)
        total: int = seconds
        minutes: int = seconds // 60
        hours: int = 0
        days: int = 0
        if minutes >= 1:
            seconds = seconds - (minutes * 60)
        if minutes // 60 >= 1:
            hours = minutes // 60
            minutes = minutes - (hours * 60)
        if hours // 24 >= 1:
            days = hours // 24
            hours = hours - (days * 24)
        return cls(total_seconds=total, years=0, months=0, days=days, hours=hours, minutes=minutes, seconds=seconds)

    @property
    def seconds(self) -> int:
        return self._seconds

    @property
    def minutes(self) -> int:
        return self._minutes

    @property
    def hours(self) -> int:
        return self._hours

    @property
    def days(self) -> int:
        return self._days

    @property
    def months(self) -> int:
        return self._months

    @property
    def years(self) -> int:
        return self._years

    def isoformat(self, fold=True):
        """ This method returns the duration in an ISO-8601 (https://en.wikipedia.org/wiki/ISO_8601#Durations) format.
        Optional parameter `fold` can be set to False (True by default) to display even the empty elements of the
        duration.

        TODO: There must be a more intelligent way to do that
        """
        _rep = "P"
        if self._years or not fold:
            _rep = f"{_rep}{self._years}Y"
        if self._months or not fold:
            _rep = f"{_rep}{self._months}M"
        if self._days or not fold:
            _rep = f"{_rep}{self._days}D"
        # From now on, it's time elements, so we must append "T"
        if (self._hours or self._minutes or self._seconds) or not fold:
            _rep = f"{_rep}T"
            if self._hours or not fold:
                _rep = f"{_rep}{self._hours}H"
            if self._minutes or not fold:
                _rep = f"{_rep}{self._minutes}M"
            if self._seconds or not fold:
                _rep = f"{_rep}{self._seconds}S"
        return _rep

    def format(self, pattern: str):
        """ Offers a way to format the representation of this Duration similar to datetime's strftime. In the _map
        dictionary below you can see which characters will be replaced by which values."""
        _map = {
            '%Y': self._years,
            '%m': self._months,
            '%d': self._days,
            '%H': self._hours,
            '%M': self._minutes,
            '%S': self._seconds
        }
        for key, value in _map.items():
            if key in pattern:
                pattern = pattern.replace(key, str(value))
        return pattern
