from abc import abstractmethod
from .base_period import AbstractPeriod


class AbstractTimePeriod(AbstractPeriod):
    """ A period of time within a 24-hour day that does not overflow into the next day.
    Implementing periods must also implement the `to_wallclock` and `to_absolute` methods which allows a TimePeriod to
    be combined with a DatePeriod to create either a WallClockPeriod or an AbsolutePeriod.
    """

    @abstractmethod
    def to_wallclock(self, other):
        ...

    @abstractmethod
    def to_absolute(self, other, timezone):
        ...