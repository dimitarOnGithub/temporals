""" This package defines the contract for the different types of periods. The interfaces here do not define specific
types for the methods' parameters or return values for the purpose of greater extensibility. It's encouraged to inherit
those interfaces and override their signatures to define specific types for the contracts.

For example, an interface specifically focused on the Python's datetime library could look like this:
|---------------------------------------------------------------------------------------|
| foo/bar/interfaces/pydatetime.py                                                      |
|---------------------------------------------------------------------------------------|
|    from temporals.interfaces import AbstractTimePeriod                                |
|    from abc import ABC, abstractmethod                                                |
|    from datetime import time, date, datetime                                          |
|                                                                                       |
|    class DTTimePeriod(AbstractTimePeriod, ABC):                                       |
|                                                                                       |
|        @abstractmethod                                                                |
|        def is_before(self, other: time | datetime | 'DTTimePeriod') -> bool:          |
|            ...                                                                        |
|---------------------------------------------------------------------------------------|
"""
from .base_period import AbstractPeriod
from .time_period import AbstractTimePeriod
from .date_period import AbstractDatePeriod
from .datetime_period import AbstractDateTimePeriod
from .period_duration import AbstractDuration


__all__ = [
    "AbstractPeriod",
    "AbstractTimePeriod",
    "AbstractDatePeriod",
    "AbstractDateTimePeriod",
    "AbstractDuration"
]
