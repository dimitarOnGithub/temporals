from abc import abstractmethod
from .base_period import AbstractPeriod


class AbstractTimePeriod(AbstractPeriod):
    """ A period of time within a 24-hour day that does not overflow into the next day. Implementing periods must also
    implement the `combine` method which allows a TimePeriod to be combined with a DatePeriod to create a DateTimePeriod
    """

    @abstractmethod
    def combine(self, other):
        ...
