from typing import Union
from temporals.interfaces import AbstractTimePeriod, AbstractDatePeriod, AbstractDateTimePeriod
from abc import ABC, abstractmethod
from datetime import time, date, datetime


class PyTimePeriod(AbstractTimePeriod, ABC):

    @property
    @abstractmethod
    def start(self) -> time:
        ...

    @property
    @abstractmethod
    def end(self) -> time:
        ...

    @abstractmethod
    def is_before(self, other: Union['PyTimePeriod', time]) -> bool:
        ...

    @abstractmethod
    def is_after(self, other: Union['PyTimePeriod', time]) -> bool:
        ...

    @abstractmethod
    def get_interim(self, other: Union['PyTimePeriod', time]) -> Union['PyTimePeriod', None]:
        ...

    @abstractmethod
    def overlaps_with(self, other: Union['PyTimePeriod', 'PyDateTimePeriod']) -> bool:
        ...

    @abstractmethod
    def overlapped_by(self, other: Union['PyTimePeriod', 'PyDateTimePeriod']) -> bool:
        ...

    @abstractmethod
    def get_overlap(self, other: Union['PyTimePeriod', 'PyDateTimePeriod']) -> Union['PyTimePeriod', None]:
        ...

    @abstractmethod
    def get_disconnect(self, other: Union['PyTimePeriod', 'PyDateTimePeriod']) -> Union['PyTimePeriod', None]:
        ...

    @abstractmethod
    def combine(self, other: Union['PyDatePeriod', date]) -> 'PyDateTimePeriod':
        ...


class PyDatePeriod(AbstractDatePeriod, ABC):

    @property
    @abstractmethod
    def start(self) -> date:
        ...

    @property
    @abstractmethod
    def end(self) -> date:
        ...

    @abstractmethod
    def is_before(self, other: Union['PyDatePeriod', 'PyDateTimePeriod', datetime, date]) -> bool:
        ...

    @abstractmethod
    def is_after(self, other: Union['PyDatePeriod', 'PyDateTimePeriod', datetime, date]) -> bool:
        ...

    @abstractmethod
    def get_interim(self, other: Union['PyDatePeriod', date]) -> Union['PyDatePeriod', None]:
        ...

    @abstractmethod
    def overlaps_with(self, other: Union['PyDatePeriod', 'PyDateTimePeriod']) -> bool:
        ...

    @abstractmethod
    def overlapped_by(self, other: Union['PyDatePeriod', 'PyDateTimePeriod']) -> bool:
        ...

    @abstractmethod
    def get_overlap(self, other: Union['PyDatePeriod', 'PyDateTimePeriod']) -> Union['PyDatePeriod', None]:
        ...

    @abstractmethod
    def get_disconnect(self, other: Union['PyDatePeriod', 'PyDateTimePeriod']) -> Union['PyDatePeriod', None]:
        ...

    @abstractmethod
    def combine(self, other: Union['PyTimePeriod', time]) -> 'PyDateTimePeriod':
        ...

    @abstractmethod
    def as_datetime(self) -> 'PyDateTimePeriod':
        ...


class PyDateTimePeriod(AbstractDateTimePeriod, ABC):

    @property
    @abstractmethod
    def start(self) -> datetime:
        ...

    @property
    @abstractmethod
    def end(self) -> datetime:
        ...

    @abstractmethod
    def is_before(self, other: Union['PyDatePeriod', 'PyDateTimePeriod', date, datetime]) -> bool:
        ...

    @abstractmethod
    def is_after(self, other: Union['PyDatePeriod', 'PyDateTimePeriod', date, datetime]) -> bool:
        ...

    @abstractmethod
    def get_interim(self, other: Union['PyDateTimePeriod', datetime]) -> Union['PyDateTimePeriod', None]:
        ...

    @abstractmethod
    def overlaps_with(self, other: Union['PyTimePeriod', 'PyDatePeriod', 'PyDateTimePeriod']) -> bool:
        ...

    @abstractmethod
    def overlapped_by(self, other: Union['PyTimePeriod', 'PyDatePeriod', 'PyDateTimePeriod']) -> bool:
        ...

    @abstractmethod
    def get_overlap(self,
                    other: Union['PyTimePeriod', 'PyDatePeriod', 'PyDateTimePeriod']
                    ) -> Union['PyTimePeriod', 'PyDatePeriod', 'PyDateTimePeriod', None]:
        ...

    @abstractmethod
    def get_disconnect(self,
                       other: Union['PyTimePeriod', 'PyDatePeriod', 'PyDateTimePeriod']
                       ) -> Union['PyTimePeriod', 'PyDatePeriod', 'PyDateTimePeriod', None]:
        ...


class PyWallClockPeriod(AbstractDateTimePeriod, ABC):
    ...


class PyAbsolutePeriod(AbstractDateTimePeriod, ABC):
    ...
