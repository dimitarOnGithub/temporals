from datetime import time, date, datetime, timedelta
from zoneinfo import ZoneInfo


class Period:

    def __init__(self,
                 start: time | date | datetime,
                 end: time | date | datetime,
                 zone_overwrite: ZoneInfo | str = None,
                 inherit_zone: bool = False
                 ):
        if start > end:
            raise ValueError(f'The start of a period cannot be before its end')
        self.start = start
        self.end = end
        self.duration = Duration(self)

    def __eq__(self, other):
        raise NotImplemented(f'Period class does not contain __eq__ method, inheriting classes must override it')

    def __contains__(self, item):
        raise NotImplemented(f'Period class does not contain __eq__ method, inheriting classes must override it')

    def __repr__(self):
        return f'Period({self.start}, {self.end})'

    def __str__(self):
        return f'{self.start}/{self.end}'


class TimePeriod(Period):

    def __init__(self, start, end, **kwargs):
        super().__init__(start, end)


class DatePeriod(Period):

    def __init__(self, start: date, end: date, **kwargs):
        super().__init__(start, end)


class DatetimePeriod(Period):

    def __init__(self, start, end, **kwargs):
        super().__init__(start, end)


class Duration:

    def __init__(self,
                 period: Period,
                 **kwargs):
        if isinstance(period.start, time) and isinstance(period.end,time):
            # OOTB datetime.time does not support operations, so we'll turn it into a timedelta
            _start = timedelta(hours=period.start.hour,
                               minutes=period.start.minute,
                               seconds=period.start.second)
            _end = timedelta(hours=period.end.hour,
                             minutes=period.end.minute,
                             seconds=period.end.second)
            td = _end - _start
        else:
            td = period.end - period.start
        # TODO: Test this and account for leap years
        self.seconds = 0
        self.hours = 0
        self.days = 0
        self.weeks = 0
        self.months = 0
        self.years = 0
        self.minutes = int(td.total_seconds() // 60)
        if self.minutes >= 1:
            self.seconds = int(td.total_seconds() - (self.minutes * 60))
        if self.minutes // 60 >= 1:
            self.hours = self.minutes // 60
            self.minutes = self.minutes - (self.hours * 60)
        if self.hours // 24 >= 1:
            self.days = self.hours // 24
            self.hours = self.hours - (self.days * 24)
        if self.days // 7 >= 1:
            self.weeks = self.days // 7
            self.days = self.days - (self.weeks * 7)
        if self.weeks // 4 >= 1:
            self.months = self.weeks // 4
            self.weeks = self.weeks - (self.months * 4)
        if self.months // 12 >= 1:
            self.years = self.months // 12
            self.months = self.months - (self.years * 12)
        """if self.days // 365 >= 1:
            self.years = self.days // 365
            self.days = self.days - (self.years * 365)"""
        print(f"P{self.years}Y{self.months}M{self.weeks}W{self.days}D{self.hours}H{self.minutes}M{self.seconds}S")
