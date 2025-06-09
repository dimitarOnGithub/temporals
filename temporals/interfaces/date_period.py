from abc import abstractmethod
from .base_period import AbstractPeriod
from .datetime_period import AbstractDateTimePeriod


class AbstractDatePeriod(AbstractPeriod):
    """ A date period that does not contain a specific time. Implementing periods must also implement two additional
    methods:
        combine - which allows combining the DatePeriod with a TimePeriod to create a DateTimePeriod
    and
        as_datetime - which creates a DateTimePeriod with its time values set to midnight for the start and 23:59 for
                the end
    """

    @abstractmethod
    def combine(self, other):
        ...

    @abstractmethod
    def as_datetime(self) -> 'AbstractDateTimePeriod':
        ...
