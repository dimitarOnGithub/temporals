from __future__ import annotations
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
    def is_before(self, other: 'PyTimePeriod' | time) -> bool:
        ...

    @abstractmethod
    def is_after(self, other: 'PyTimePeriod' | time) -> bool:
        ...

    @abstractmethod
    def get_interim(self, other: 'PyTimePeriod' | time) -> 'PyTimePeriod' | None:
        ...

    @abstractmethod
    def overlaps_with(self, other: 'PyTimePeriod' | 'PyWallClockPeriod' | 'PyAbsolutePeriod') -> bool:
        ...

    @abstractmethod
    def overlapped_by(self, other: 'PyTimePeriod' | 'PyWallClockPeriod' | 'PyAbsolutePeriod') -> bool:
        ...

    @abstractmethod
    def get_overlap(self,other: 'PyTimePeriod' | 'PyWallClockPeriod' | 'PyAbsolutePeriod') -> 'PyTimePeriod' | None:
        ...

    @abstractmethod
    def get_disconnect(self, other: 'PyTimePeriod' | 'PyWallClockPeriod' | 'PyAbsolutePeriod') -> 'PyTimePeriod' | None:
        ...

    @abstractmethod
    def to_wallclock(self, other: 'PyDatePeriod' | date) -> 'PyWallClockPeriod':
        ...

    @abstractmethod
    def to_absolute(self, other: 'PyDatePeriod' | date, timezone: ZoneInfo) -> 'PyAbsolutePeriod':
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
    def is_before(self, other: 'PyDatePeriod' | 'PyWallClockPeriod' | 'PyAbsolutePeriod' | datetime | date) -> bool:
        ...

    @abstractmethod
    def is_after(self, other: 'PyDatePeriod' | 'PyWallClockPeriod' | 'PyAbsolutePeriod' | datetime | date) -> bool:
        ...

    @abstractmethod
    def get_interim(self, other: 'PyDatePeriod' | date) -> 'PyDatePeriod' | None:
        ...

    @abstractmethod
    def overlaps_with(self, other: 'PyDatePeriod' | 'PyWallClockPeriod' | 'PyAbsolutePeriod') -> bool:
        ...

    @abstractmethod
    def overlapped_by(self, other: 'PyDatePeriod' | 'PyWallClockPeriod' | 'PyAbsolutePeriod') -> bool:
        ...

    @abstractmethod
    def get_overlap(self, other: 'PyDatePeriod' | 'PyWallClockPeriod' | 'PyAbsolutePeriod') -> 'PyDatePeriod' | None:
        ...

    @abstractmethod
    def get_disconnect(self, other: 'PyDatePeriod' | 'PyWallClockPeriod' | 'PyAbsolutePeriod') -> 'PyDatePeriod' | None:
        ...

    @abstractmethod
    def to_wallclock(self, other: 'PyTimePeriod' | time) -> 'PyWallClockPeriod':
        ...

    @abstractmethod
    def to_absolute(self, other: 'PyTimePeriod' | time, timezone: ZoneInfo) -> 'PyAbsolutePeriod':
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
    def is_before(self, other: 'PyDatePeriod' | 'PyWallClockPeriod' | date | datetime) -> bool:
        ...

    @abstractmethod
    def is_after(self, other: 'PyDatePeriod' | 'PyWallClockPeriod' | date | datetime) -> bool:
        ...

    @abstractmethod
    def get_interim(self, other: 'PyWallClockPeriod' | datetime) -> 'PyWallClockPeriod' | None:
        ...

    @abstractmethod
    def overlaps_with(self, other: 'PyTimePeriod' | 'PyDatePeriod' | 'PyWallClockPeriod') -> bool:
        ...

    @abstractmethod
    def overlapped_by(self, other: 'PyTimePeriod' | 'PyDatePeriod' | 'PyWallClockPeriod') -> bool:
        ...

    @abstractmethod
    def get_overlap(self,
                    other: 'PyTimePeriod' | 'PyDatePeriod' | 'PyWallClockPeriod'
                    ) -> 'PyTimePeriod' | 'PyDatePeriod' | 'PyWallClockPeriod' | None:
        ...

    @abstractmethod
    def get_disconnect(self,
                       other: 'PyTimePeriod' | 'PyDatePeriod' | 'PyWallClockPeriod'
                       ) -> 'PyTimePeriod' | 'PyDatePeriod' | 'PyWallClockPeriod' | None:
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
    def is_before(self, other: 'PyDatePeriod' | 'PyAbsolutePeriod' | date | datetime) -> bool:
        ...

    @abstractmethod
    def is_after(self, other: 'PyDatePeriod' | 'PyAbsolutePeriod' | date | datetime) -> bool:
        ...

    @abstractmethod
    def get_interim(self, other: 'PyAbsolutePeriod' | datetime) -> 'PyAbsolutePeriod' | None:
        ...

    @abstractmethod
    def overlaps_with(self, other: 'PyTimePeriod' | 'PyDatePeriod' | 'PyAbsolutePeriod') -> bool:
        ...

    @abstractmethod
    def overlapped_by(self, other: 'PyTimePeriod' | 'PyDatePeriod' | 'PyAbsolutePeriod') -> bool:
        ...

    @abstractmethod
    def get_overlap(self,
                    other: 'PyTimePeriod' | 'PyDatePeriod' | 'PyAbsolutePeriod'
                    ) -> 'PyTimePeriod' | 'PyDatePeriod' | 'PyAbsolutePeriod' | None:
        ...

    @abstractmethod
    def get_disconnect(self,
                       other: 'PyTimePeriod' | 'PyDatePeriod' | 'PyAbsolutePeriod'
                       ) -> 'PyTimePeriod' | 'PyDatePeriod' | 'PyAbsolutePeriod' | None:
        ...
