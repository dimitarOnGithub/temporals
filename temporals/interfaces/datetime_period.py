from abc import ABC
from .base_period import AbstractPeriod


class AbstractDateTimePeriod(AbstractPeriod, ABC):
    """ A period that contains a date and a time """


class WallClockDateTimePeriod(AbstractDateTimePeriod, ABC):
    """ A datetime period whose duration corresponds to the clock on the wall even if there's a DST change """


class AbsoluteDateTimePeriod(AbstractDateTimePeriod, ABC):
    """ A datetime period whose duration accounts for any clock changes (shift forward/back) and updates its duration
    to reflect that change """