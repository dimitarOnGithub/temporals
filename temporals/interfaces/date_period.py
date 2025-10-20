from abc import abstractmethod
from .base_period import AbstractPeriod


class AbstractDatePeriod(AbstractPeriod):
    """ A date period that does not contain a specific time. Implementing periods must also implement two additional
    methods:
        to_wallclock - which allows combining the DatePeriod with a TimePeriod or a datetime.time object to create
            a WallClockPeriod
        to_absolute - which allows combining the DatePeriod with a TimePeriod or a datetime.time object to create
            an AbsolutePeriod
    """

    @abstractmethod
    def to_wallclock(self, other):
        ...

    @abstractmethod
    def to_absolute(self, other, timezone):
        ...
