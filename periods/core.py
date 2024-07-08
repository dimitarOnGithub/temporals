from datetime import time, date, datetime, timedelta, tzinfo
from typing import Union
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
        self.duration = Duration(period=self)

    def __eq__(self, other):
        raise NotImplemented(f'Period class does not contain __eq__ method, inheriting classes must override it')

    def __contains__(self, item):
        raise NotImplemented(f'Period class does not contain __eq__ method, inheriting classes must override it')

    def __lt__(self, other):
        raise NotImplemented(f'Period class does not contain __lt__ method, inheriting classes must override it')

    def __gt__(self, other):
        raise NotImplemented(f'Period class does not contain __lt__ method, inheriting classes must override it')

    def __repr__(self):
        return f"{self.__class__.__name__}(start={self.start.__repr__()}, {self.end.__repr__()})"

    def __str__(self):
        return f'{self.start}/{self.end}'


class TimePeriod(Period):
    """ The TimePeriod class is responsible for time periods within a 24-hour day. Instances of this class offer the
    'equal' comparison (see __eq__ below), as well as the membership (is, is not) test operators (see __contains__)
    below.
    """

    def __init__(self,
                 start: time,
                 end: time,
                 **kwargs):
        super().__init__(start, end)

    def __eq__(self, other):
        """ Equality can only be determined between instances of this class, as well as the DatetimePeriod class, since
        only these two classes contain information about the actual time in a day. In both cases, the instances will
        be tested for equal start and end times.

        # TODO: more docs when extra methods
        """
        if isinstance(other, DatetimePeriod):
            return (self.start == other.start.time()
                    and self.end == other.end.time())
        if isinstance(other, TimePeriod):
            return (self.start == other.start
                    and self.end == other.end)
        return False

    def __contains__(self, item):
        """ Membership test can be done with instances of this class, the DatetimePeriod class, datetime.datetime and
        datetime.time objects; When membership test is done for a period, it assumes that the request is to check if
        the tested period exists WITHIN the temporal borders of this period, that is to say, whether the start and
        end times of the other period are after and before, respectively, of the same of this period.

        If you have an instance of this period, for example:
        >>> start = time(8, 0, 0)  # 8 o'clock in the morning
        >>> end = time(17, 0, 0)  # 5 o'clock in the afternoon
        >>> workday = TimePeriod(start=start, end=end)

        and then another TimePeriod:
        >>> lunch_start = time(12, 0, 0)  # 12 o'clock at lunch
        >>> lunch_end = time(13, 0, 0)  # 1 o'clock in the afternoon
        >>> lunch_break = TimePeriod(start=lunch_start, end=lunch_end)

        Then you can check if the lunch_break period is within your workday period:
        >>> lunch_break in workday

        For more in-depth comparisons and functionality, see:
            is_part_of
            has_as_part
            overlap
            disconnect
        """
        if isinstance(item, TimePeriod):
            """ Only return True if the start and end times of `item` are within the actual time duration of this 
            period.
            """
            return item.start > self.start and item.end < self.end
        if isinstance(item, DatetimePeriod):
            return item.start.time() > self.start and item.end.time() < self.end
        if isinstance(item, datetime):
            item = item.time()
        if isinstance(item, time):
            return self.start < item < self.end
        return False

    def __lt__(self, other):
        # TODO: think about if < makes sense
        pass

    def __gt__(self, other):
        # TODO: think about if > makes sense
        pass

    def is_part_of(self,
                   other: Union['TimePeriod', 'DatetimePeriod']) -> bool:
        # TODO: Docs
        if self not in other:
            return False
        other_start: time = None
        other_end: time = None
        if isinstance(other, TimePeriod):
            other_start = other.start
            other_end = other.end
        if isinstance(other, DatetimePeriod):
            other_start = other.start.time()
            other_end = other.end.time()
        if other_start < self.start or self.end > other_end:
            return True
        return False

    def has_as_part(self,
                    other: Union['TimePeriod', 'DatetimePeriod']) -> bool:
        # TODO: docs
        pass


class DatePeriod(Period):

    def __init__(self, start: date, end: date, **kwargs):
        super().__init__(start, end)


class DatetimePeriod(Period):

    def __init__(self, start, end, **kwargs):
        super().__init__(start, end)


class Duration:

    def __init__(self,
                 period: Period = None,
                 start: time | date | datetime = None,
                 end: time | date | datetime = None):
        if period:
            if isinstance(period, Period) or issubclass(type(period), Period):
                self.period: Period = period
                self.start = period.start
                self.end = period.end
            else:
                raise ValueError(f"Provided object '{period}' is not an instance or child of {Period}")
        if start and end:
            self.period = None
            if not isinstance(start, (time, date, datetime)):
                raise ValueError(f"Provided value '{start}' for start is not an instance of datetime.time, "
                                 f"datetime.date or datetime.datetime")
            self.start = start
            if not isinstance(end, (time, date, datetime)):
                raise ValueError(f"Provided value '{end}' for end is not an instance of datetime.time, "
                                 f"datetime.date or datetime.datetime")
            self.end = end
        if isinstance(self.start, time) and isinstance(self.end, time):
            # OOTB datetime.time does not support operations, so we'll turn it into a timedelta
            _start = timedelta(hours=self.start.hour,
                               minutes=self.start.minute,
                               seconds=self.start.second)
            _end = timedelta(hours=self.end.hour,
                             minutes=self.end.minute,
                             seconds=self.end.second)
            self.timedelta = _end - _start
        else:
            self.timedelta = self.end - self.start
        # TODO: Test this and account for leap years
        self.seconds: int = 0
        self.hours: int = 0
        self.days: int = 0
        self.weeks: int = 0
        self.months: int = 0
        self.years: int = 0
        self.minutes: int = int(self.timedelta.total_seconds() // 60)
        if self.minutes >= 1:
            self.seconds = int(self.timedelta.total_seconds() - (self.minutes * 60))
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

    def __str__(self):
        return self.isoformat(fold=False)

    def __repr__(self):
        if self.period:
            return f'Duration(period={self.period.__repr__()})'
        else:
            return f'Duration(start={self.start.__repr__()}, end={self.end.__repr__()})'

    def isoformat(self, fold=True):
        """ TODO: Docs; There must be a more intelligent way to do that """
        _rep = "P"
        if self.years or not fold:
            _rep = f"{_rep}{self.years}Y"
        if self.months or not fold:
            _rep = f"{_rep}{self.months}M"
        if self.weeks or not fold:
            _rep = f"{_rep}{self.weeks}W"
        if self.days or not fold:
            _rep = f"{_rep}{self.days}D"
        # From now on, it's time elements, so we must append "T"; This is a bug if the duration has no time.
        _rep = f"{_rep}T"
        if self.hours or not fold:
            _rep = f"{_rep}{self.hours}H"
        if self.minutes or not fold:
            _rep = f"{_rep}{self.minutes}M"
        if self.seconds or not fold:
            _rep = f"{_rep}{self.seconds}S"
        return _rep

    def format(self, pattern, fold=False):
        # TODO: Implement
        pass
