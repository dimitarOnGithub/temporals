from abc import ABC
from .base_period import AbstractPeriod


class AbstractWallClockPeriod(AbstractPeriod, ABC):
    """ A datetime period whose duration corresponds to the clock on the wall even if there's a DST change """


class AbstractAbsolutePeriod(AbstractPeriod, ABC):
    """ A datetime period whose duration accounts for any clock changes (shift forward/back) and updates its duration
    to reflect that change """
