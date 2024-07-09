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
        return f"{self.__class__.__name__}(start={self.start.__repr__()}, end={self.end.__repr__()})"

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
        if not isinstance(start, time):
            raise ValueError(f"Provided value '{start}' for parameter 'start' is not an instance of time")
        if not isinstance(end, time):
            raise ValueError(f"Provided value '{end}' for parameter 'end' is not an instance of time")
        super().__init__(start, end)

    def __eq__(self, other):
        """ Equality can only be determined between instances of this class, as well as the DatetimePeriod class, since
        only these two classes contain information about the actual time in a day. In both cases, the instances will
        be tested for exactly equal start and end times.

        This method does not account for overlaps between the start and end times of the periods, to get this
        functionality, look at the following methods:
            overlaps_with
            overlapped_by
            get_overlap
            get_disconnect
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

        0800       Your period:          1700
        |==================================|
             1200 |=============| 1300
                         ^ The period you are testing

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
            return self.start <= item.start and item.end <= self.end
        if isinstance(item, DatetimePeriod):
            return item.start.time() >= self.start and item.end.time() <= self.end
        if isinstance(item, datetime):
            item = item.time()
        if isinstance(item, time):
            return self.start <= item <= self.end
        return False

    def __lt__(self, other):
        # TODO: think about if < makes sense
        pass

    def __gt__(self, other):
        # TODO: think about if > makes sense
        pass

    def overlaps_with(self,
                      other: Union['TimePeriod', 'DatetimePeriod']
                      ) -> bool:
        """ Test if this period overlaps with another period that has begun before this one. This check will evaluate
        as True in the following scenario:
                        1000       This period:          1700
                        |==================================|
             0800 |=============| 1300
                         ^ The other period

        >>> this_start = time(10, 0, 0)
        >>> this_end = time(17, 0, 0)
        >>> other_start = (8, 0, 0)
        >>> other_end = (13, 0, 0)
        >>> this_period = TimePeriod(start=this_start, end=this_end)
        >>> other_period = TimePeriod(start=other_start, end=other_end)
        >>> this_period.overlaps_with(other_period)
        True

        The period that has begun first is considered the "main" period, even if it finishes before the end of this
        period, since it occupies an earlier point in time. Therefore, the current period, which has begun at a later
        point in time, is considered to be the overlapping one. Hence, the opposite check (overlapped_by) is True for
        the other_period:
        >>> other_period.overlapped_by(this_period)
        True

        Note that both of these checks will only work for partially overlapping periods - for fully overlapping periods,
        use the `in` membership test:
        >>> this_period in other_period
        """
        other_start: time = None
        other_end: time = None
        if isinstance(other, TimePeriod):
            other_start = other.start
            other_end = other.end
        if isinstance(other, DatetimePeriod):
            other_start = other.start.time()
            other_end = other.end.time()
        if other_start < self.start and other_end < self.end:
            return True
        return False

    def overlapped_by(self,
                      other: Union['TimePeriod', 'DatetimePeriod']
                      ) -> bool:
        """ Test if this period is overlapped by the other period. This check will evaluate True in the following
        scenario:
           1000       This period:          1700
            |==================================|
                                1500 |=============| 1800
                                            ^ The other period

        >>> this_start = time(10, 0, 0)
        >>> this_end = time(17, 0, 0)
        >>> other_start = (15, 0, 0)
        >>> other_end = (18, 0, 0)
        >>> this_period = TimePeriod(start=this_start, end=this_end)
        >>> other_period = TimePeriod(start=other_start, end=other_end)
        >>> this_period.overlapped_by(other_period)
        True

        Since this period has begun first, it is considered the "main" one, and all other periods that begin after this
        one, are considered to be overlapping it. Therefore, the opposite check, `overlaps_with`, will evaluate True
        if the opposite check is being made:
        >>> other_period.overlaps_with(this_period)
        True

        Note that both of these checks will only work for partially overlapping periods - for fully overlapping periods,
        use the `in` membership test:
        >>> this_period in other_period
        """
        other_start: time = None
        other_end: time = None
        if isinstance(other, TimePeriod):
            other_start = other.start
            other_end = other.end
        if isinstance(other, DatetimePeriod):
            other_start = other.start.time()
            other_end = other.end.time()
        if self.start < other_start and self.end < other_end:
            return True
        return False

    def get_overlap(self,
                    other: Union['TimePeriod', 'DatetimePeriod']
                    ) -> Union['TimePeriod', None]:
        """ Method returns the overlapping interval between the two periods as a new TimePeriod instance

        >>> period1_start = time(8, 0, 0)
        >>> period1_end = time(12, 0, 0)
        >>> period1 = TimePeriod(start=period1_start, end=period1_end)
        >>> period2_start = time(10, 0, 0)
        >>> period2_end = time(13, 0, 0)
        >>> period2 = TimePeriod(start=period2_start, end=period2_end)
        >>> period1
        TimePeriod(start=datetime.time(8, 0), end=datetime.time(12, 0))
        >>> period2
        TimePeriod(start=datetime.time(10, 0), end=datetime.time(13, 0))

        On a timeline, the two periods can be illustrated as:
           0800              Period 1                1200
            |=========================================|
                               |============================|
                              1000       Period 2          1300

        As expected, attempting a membership test would return False:
        >>> period2 in period1
        False
        however, testing overlaps does return True:
        >>> period1.overlapped_by(period2)
        True
        and the opposite:
        >>> period2.overlaps_with(period1)
        True

        Therefore, we can use the `get_overlap` method to obtain the precise length of the overlapping interval:
        >>> period1.get_overlap(period2)
        TimePeriod(start=datetime.time(10, 0), end=datetime.time(12, 0))
        And since the overlap is always the same, regardless of the observer, the opposite action would have the same
        result:
        >>> period2.get_overlap(period1)
        TimePeriod(start=datetime.time(10, 0), end=datetime.time(12, 0))
        """
        if not isinstance(other, TimePeriod) or not isinstance(other, DatetimePeriod):
            raise TypeError(f"Cannot perform temporal operations with instances of type '{type(other)}'")
        if self.overlaps_with(other):
            end_time = other.end if isinstance(other, TimePeriod) else other.end.time()
            return TimePeriod(start=self.start, end=end_time)
        elif self.overlapped_by(other):
            start_time = other.start if isinstance(other, TimePeriod) else other.start.time()
            return TimePeriod(start=start_time, end=self.end)

    def get_disconnect(self,
                       other: Union['TimePeriod', 'DatetimePeriod']
                       ) -> Union['TimePeriod', None]:
        """ Method returns the disconnect interval from the point of view of the invoking period. This means the time
        disconnect from the start of this period until the start of the period to which this period is being compared
        to. Since the span of time is relative to each of the two periods, this method will always return different
        intervals.

        Take, for example, the following two periods:
        >>> period1_start = time(8, 0, 0)
        >>> period1_end = time(12, 0, 0)
        >>> period1 = TimePeriod(start=period1_start, end=period1_end)
        >>> period2_start = time(10, 0, 0)
        >>> period2_end = time(13, 0, 0)
        >>> period2 = TimePeriod(start=period2_start, end=period2_end)
        >>> period1
        TimePeriod(start=datetime.time(8, 0), end=datetime.time(12, 0))
        >>> period2
        TimePeriod(start=datetime.time(10, 0), end=datetime.time(13, 0))

        On a timeline, the two periods can be illustrated as:
           0800              Period 1                1200
            |=========================================|
                               |============================|
                              1000       Period 2          1300

        From the point of view of Period 1, the disconnect between the two periods is between the time 0800 and 1000;
        however, from the point of view of Period 2, the disconnect between them is between the time 1200 and 1300.

        Therefore, if you want to obtain the amount of time when the periods do NOT overlap as relative to Period 1,
        you should use:
        >>> period1.get_disconnect(period2)
        TimePeriod(start=datetime.time(8, 0), end=datetime.time(10, 0))

        But if you want to obtain the same as relative to Period 2 instead:
        >>> period2.get_disconnect(period1)
        TimePeriod(start=datetime.time(12, 0), end=datetime.time(13, 0))
        """
        if not isinstance(other, TimePeriod) and not isinstance(other, DatetimePeriod):
            raise TypeError(f"Cannot perform temporal operations with instances of type '{type(other)}'")
        if self.overlapped_by(other):
            end_time = other.start if isinstance(other, TimePeriod) else other.start.time()
            return TimePeriod(start=self.start, end=end_time)
        elif self.overlaps_with(other):
            start_time = other.end if isinstance(other, TimePeriod) else other.end.time()
            return TimePeriod(start=start_time, end=self.end)


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
