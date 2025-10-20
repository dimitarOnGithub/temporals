from abc import abstractmethod
from .base_period import AbstractPeriod
from .datetime_period import AbstractAbsolutePeriod, AbstractWallClockPeriod


class AbstractTimePeriod(AbstractPeriod):
    """ A period of time within a 24-hour day that does not overflow into the next day.
    Implementing periods must also implement the `to_wallclock` and `to_absolute` methods which allows a TimePeriod to
    be combined with a DatePeriod to create either a WallClockPeriod or an AbsolutePeriod.
    """

    @abstractmethod
    def to_wallclock(self, other) -> AbstractWallClockPeriod:
        """ Implementing classes must provide the ability to create an instance of the AbstractWallClockPeriod interface """
        ...

    @abstractmethod
    def to_absolute(self, other, timezone) -> AbstractAbsolutePeriod:
        """ Implementing classes must provide the ability to create an instance of the AbstractAbsolutePeriod interface """
        ...
