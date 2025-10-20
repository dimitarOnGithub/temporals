from typing import Union
from zoneinfo import ZoneInfo
from temporals.interfaces import AbstractTimePeriod, AbstractDatePeriod, AbstractAbsolutePeriod, AbstractWallClockPeriod
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
    def overlaps_with(self, other: Union['PyTimePeriod', 'PyWallClockPeriod', 'PyAbsolutePeriod']) -> bool:
        ...

    @abstractmethod
    def overlapped_by(self, other: Union['PyTimePeriod', 'PyWallClockPeriod', 'PyAbsolutePeriod']) -> bool:
        ...

    @abstractmethod
    def get_overlap(self, other: Union['PyTimePeriod', 'PyWallClockPeriod', 'PyAbsolutePeriod']
                    ) -> Union['PyTimePeriod', None]:
        ...

    @abstractmethod
    def get_disconnect(self, other: Union['PyTimePeriod', 'PyWallClockPeriod', 'PyAbsolutePeriod']
                       ) -> Union['PyTimePeriod', None]:
        ...

    @abstractmethod
    def to_wallclock(self, other: Union['PyDatePeriod', date]) -> 'PyWallClockPeriod':
        ...

    @abstractmethod
    def to_absolute(self, other: Union['PyDatePeriod', date], timezone: ZoneInfo) -> 'PyAbsolutePeriod':
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
    def is_before(self, other: Union['PyDatePeriod', 'PyWallClockPeriod', 'PyAbsolutePeriod', datetime, date]) -> bool:
        ...

    @abstractmethod
    def is_after(self, other: Union['PyDatePeriod', 'PyWallClockPeriod', 'PyAbsolutePeriod', datetime, date]) -> bool:
        ...

    @abstractmethod
    def get_interim(self, other: Union['PyDatePeriod', date]) -> Union['PyDatePeriod', None]:
        ...

    @abstractmethod
    def overlaps_with(self, other: Union['PyDatePeriod', 'PyWallClockPeriod', 'PyAbsolutePeriod']) -> bool:
        ...

    @abstractmethod
    def overlapped_by(self, other: Union['PyDatePeriod', 'PyWallClockPeriod', 'PyAbsolutePeriod']) -> bool:
        ...

    @abstractmethod
    def get_overlap(self, other: Union['PyDatePeriod', 'PyWallClockPeriod', 'PyAbsolutePeriod']
                    ) -> Union['PyDatePeriod', None]:
        ...

    @abstractmethod
    def get_disconnect(self, other: Union['PyDatePeriod', 'PyWallClockPeriod', 'PyAbsolutePeriod']
                       ) -> Union['PyDatePeriod', None]:
        ...

    @abstractmethod
    def to_wallclock(self, other: Union['PyTimePeriod', time]) -> 'PyWallClockPeriod':
        ...

    @abstractmethod
    def to_absolute(self, other: Union['PyTimePeriod', time], timezone: ZoneInfo) -> 'PyAbsolutePeriod':
        ...


class PyWallClockPeriod(AbstractWallClockPeriod, ABC):

    @property
    @abstractmethod
    def start(self) -> datetime:
        ...

    @property
    @abstractmethod
    def end(self) -> datetime:
        ...

    @abstractmethod
    def is_before(self, other: Union['PyDatePeriod', 'PyWallClockPeriod', date, datetime]) -> bool:
        ...

    @abstractmethod
    def is_after(self, other: Union['PyDatePeriod', 'PyWallClockPeriod', date, datetime]) -> bool:
        ...

    @abstractmethod
    def get_interim(self, other: Union['PyWallClockPeriod', datetime]) -> Union['PyWallClockPeriod', None]:
        ...

    @abstractmethod
    def overlaps_with(self, other: Union['PyTimePeriod', 'PyDatePeriod', 'PyWallClockPeriod']) -> bool:
        ...

    @abstractmethod
    def overlapped_by(self, other: Union['PyTimePeriod', 'PyDatePeriod', 'PyWallClockPeriod']) -> bool:
        ...

    @abstractmethod
    def get_overlap(self,
                    other: Union['PyTimePeriod', 'PyDatePeriod', 'PyWallClockPeriod']
                    ) -> Union['PyTimePeriod', 'PyDatePeriod', 'PyWallClockPeriod', None]:
        ...

    @abstractmethod
    def get_disconnect(self,
                       other: Union['PyTimePeriod', 'PyDatePeriod', 'PyWallClockPeriod']
                       ) -> Union['PyTimePeriod', 'PyDatePeriod', 'PyWallClockPeriod', None]:
        ...


class PyAbsolutePeriod(AbstractAbsolutePeriod, ABC):

    @property
    @abstractmethod
    def start(self) -> datetime:
        ...

    @property
    @abstractmethod
    def end(self) -> datetime:
        ...

    @abstractmethod
    def is_before(self, other: Union['PyDatePeriod', 'PyAbsolutePeriod', date, datetime]) -> bool:
        ...

    @abstractmethod
    def is_after(self, other: Union['PyDatePeriod', 'PyAbsolutePeriod', date, datetime]) -> bool:
        ...

    @abstractmethod
    def get_interim(self, other: Union['PyAbsolutePeriod', datetime]) -> Union['PyAbsolutePeriod', None]:
        ...

    @abstractmethod
    def overlaps_with(self, other: Union['PyTimePeriod', 'PyDatePeriod', 'PyAbsolutePeriod']) -> bool:
        ...

    @abstractmethod
    def overlapped_by(self, other: Union['PyTimePeriod', 'PyDatePeriod', 'PyAbsolutePeriod']) -> bool:
        ...

    @abstractmethod
    def get_overlap(self,
                    other: Union['PyTimePeriod', 'PyDatePeriod', 'PyAbsolutePeriod']
                    ) -> Union['PyTimePeriod', 'PyDatePeriod', 'PyAbsolutePeriod', None]:
        ...

    @abstractmethod
    def get_disconnect(self,
                       other: Union['PyTimePeriod', 'PyDatePeriod', 'PyAbsolutePeriod']
                       ) -> Union['PyTimePeriod', 'PyDatePeriod', 'PyAbsolutePeriod', None]:
        ...
