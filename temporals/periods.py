from datetime import time, date, datetime, timedelta
from typing import Union
from .exceptions import TimeAmbiguityError


class Period:

    def __init__(self,
                 start: time | date | datetime,
                 end: time | date | datetime
                 ):
        if start > end:
            raise ValueError('The start of a period cannot be before its end')
        self.start = start
        self.end = end
        self.duration = Duration(period=self)

    def __eq__(self, other):
        raise NotImplementedError('Period class does not contain __eq__ method, inheriting classes must override it')

    def __contains__(self, item):
        raise NotImplementedError('Period class does not contain __eq__ method, inheriting classes must override it')

    def __lt__(self, other):
        raise NotImplementedError('Period class does not contain __lt__ method, inheriting classes must override it')

    def __gt__(self, other):
        raise NotImplementedError('Period class does not contain __lt__ method, inheriting classes must override it')

    def __repr__(self):
        return f"{self.__class__.__name__}(start={self.start.__repr__()}, end={self.end.__repr__()})"

    def __str__(self):
        return f'{self.start.isoformat()}/{self.end.isoformat()}'


class TimePeriod(Period):
    """ The TimePeriod class is responsible for time periods within a 24-hour day. Instances of this class offer the
    'equal' comparison (see __eq__ below), as well as the membership (is, is not) test operators (see __contains__)
    below.
    """

    def __init__(self,
                 start: time,
                 end: time,
                 ):
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
        >>> other_start = time(8, 0, 0)
        >>> other_end = time(13, 0, 0)
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
        if not other_end < self.start and other_start < self.start and other_end < self.end:
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
        >>> other_start = time(15, 0, 0)
        >>> other_end = time(18, 0, 0)
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
        if not self.end < other_start and self.start < other_start and self.end < other_end:
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
        if not isinstance(other, TimePeriod) and not isinstance(other, DatetimePeriod):
            raise TypeError(f"Cannot perform temporal operations with instances of type '{type(other)}'")
        if isinstance(other, DatetimePeriod):
            return other.get_overlap(self)
        # TODO: refactor this
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
    """ The DatePeriod class is responsible for date periods containing a year, month and day. Instances of this class
    offer the 'equal' comparison (see __eq__ below), as well as the membership (is, is not) test operators
    (see __contains__) below.
    """

    def __init__(self,
                 start: date,
                 end: date,
                 ):
        if not isinstance(start, date) or isinstance(start, datetime):
            raise ValueError(f"Provided value '{start}' for parameter 'start' is not an instance of datetime.date")
        if not isinstance(end, date) or isinstance(end, datetime):
            raise ValueError(f"Provided value '{end}' for parameter 'end' is not an instance of datetime.date")
        super().__init__(start, end)

    def __eq__(self, other):
        """ Equality can only be determined between instances of this class, as well as the DatetimePeriod class, since
        only these two classes contain information about the actual date. In both cases, the instances will be tested
        for exactly equal start and end dates.

        This method does not account for overlaps between the start and end dates of the periods, to get this
        functionality, look at the following methods:
            overlaps_with
            overlapped_by
            get_overlap
            get_disconnect
        """
        if isinstance(other, DatetimePeriod):
            return (self.start == other.start.date()
                    and self.end == other.end.date())
        if isinstance(other, DatePeriod):
            return (self.start == other.start
                    and self.end == other.end)
        return False

    def __contains__(self, item):
        """ Membership test can be done with instances of this class, the DatetimePeriod class, datetime.datetime and
        datetime.date objects; When membership test is done for a period, it assumes that the request is to check if
        the tested period exists WITHIN the temporal borders of this period, that is to say, whether the start and
        end date of the other period are after and before, respectively, of the same of this period.

        2024-01-01 Your period:        2024-03-01
        |==================================|
                |=============|     <---- The period you are testing
           2024-02-01     2024-02-10

        If you have an instance of this period, for example:
        >>> start = date(2024, 7, 1)  # 1st of July 2024
        >>> end = date(2024, 9, 1)  # 1st of September 2024
        >>> holiday = DatePeriod(start=start, end=end)

        and then another DatePeriod:
        >>> departure = date(2024, 7, 10)  # 10th of July 2024
        >>> arrival = date(2024, 7, 20)  # 20th of July 2024
        >>> paris_visit = DatePeriod(start=departure, end=arrival)

        Then you can check if the lunch_break period is within your workday period:
        >>> paris_visit in holiday

        For more in-depth comparisons and functionality, see:
            overlaps_with
            overlapped_by
            get_overlap
            get_disconnect
        """
        if isinstance(item, DatePeriod):
            """ Only return True if the start and end times of `item` are within the actual time duration of this 
            period.
            """
            return self.start <= item.start and item.end <= self.end
        if isinstance(item, DatetimePeriod):
            return item.start.date() >= self.start and item.end.date() <= self.end
        if isinstance(item, datetime):
            item = item.date()
        if isinstance(item, date):
            return self.start <= item <= self.end
        return False

    def overlaps_with(self,
                      other: Union['DatePeriod', 'DatetimePeriod']
                      ) -> bool:
        """ Test if this period overlaps with another period that has begun before this one. This check will evaluate
        as True in the following scenario:
                    2024-02-01      This period:      2024-03-01
                        |==================================|
                 |=============|   <------ The other period
            2024-01-15    2024-02-05

        >>> this_start = date(2024, 2, 1)  # 2nd of Feb 2024
        >>> this_end = date(2024, 3, 1)  # 1st of Mar 2024
        >>> other_start = date(2024, 1, 15)  # 15th of Jan 2024
        >>> other_end = date(2024, 2, 5)  # 5th of Feb 2024
        >>> this_period = DatePeriod(start=this_start, end=this_end)
        >>> other_period = DatePeriod(start=other_start, end=other_end)
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
        other_start: date = None
        other_end: date = None
        if isinstance(other, DatePeriod):
            other_start = other.start
            other_end = other.end
        if isinstance(other, DatetimePeriod):
            other_start = other.start.date()
            other_end = other.end.date()
        if not other_end < self.start and other_start < self.start and other_end < self.end:
            return True
        return False

    def overlapped_by(self,
                      other: Union['DatePeriod', 'DatetimePeriod']
                      ) -> bool:
        """ Test if this period is overlapped by the other period. This check will evaluate True in the following
        scenario:
           2024-01-01      This period:      2024-01-31
                |==================================|
                                            |=============|   <------ The other period
                                        2024-01-20    2024-03-10

        >>> this_start = date(2024, 1, 1)
        >>> this_end = date(2024, 1, 31)
        >>> other_start = date(2024, 1, 20)
        >>> other_end = date(2024, 3, 10)
        >>> this_period = DatePeriod(start=this_start, end=this_end)
        >>> other_period = DatePeriod(start=other_start, end=other_end)
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
        other_start: date = None
        other_end: date = None
        if isinstance(other, DatePeriod):
            other_start = other.start
            other_end = other.end
        if isinstance(other, DatetimePeriod):
            other_start = other.start.date()
            other_end = other.end.date()
        if not self.end < other_start and self.start < other_start and self.end < other_end:
            return True
        return False

    def get_overlap(self,
                    other: Union['DatePeriod', 'DatetimePeriod']
                    ) -> Union['DatePeriod', None]:
        """ Method returns the overlapping interval between the two periods as a new DatePeriod instance

        >>> period1_start = date(2024, 1, 1)
        >>> period1_end = date(2024, 1, 10)
        >>> period1 = DatePeriod(start=period1_start, end=period1_end)
        >>> period2_start = date(2024, 1, 5)
        >>> period2_end = date(2024, 1, 15)
        >>> period2 = DatePeriod(start=period2_start, end=period2_end)
        >>> period1
        DatePeriod(start=datetime.date(2024, 1, 1), end=datetime.date(2024, 1, 10))
        >>> period2
        DatePeriod(start=datetime.date(2024, 1, 5), end=datetime.date(2024, 1, 15))

        On a timeline, the two periods can be illustrated as:
        2024-01-01      Period 1                2024-01-10
            |=========================================|
                               |============================================|
                         2024-01-05             Period 2              2024-01-15

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
        if not isinstance(other, DatePeriod) and not isinstance(other, DatetimePeriod):
            raise TypeError(f"Cannot perform temporal operations with instances of type '{type(other)}'")
        if self.overlaps_with(other):
            end_date = other.end if isinstance(other, DatePeriod) else other.end.date()
            return DatePeriod(start=self.start, end=end_date)
        elif self.overlapped_by(other):
            start_date = other.start if isinstance(other, DatePeriod) else other.start.date()
            return DatePeriod(start=start_date, end=self.end)

    def get_disconnect(self,
                       other: Union['DatePeriod', 'DatetimePeriod']
                       ) -> Union['DatePeriod', None]:
        """ Method returns the disconnect interval from the point of view of the invoking period. This means the time
        disconnect from the start of this period until the start of the period to which this period is being compared
        to. Since the span of time is relative to each of the two periods, this method will always return different
        intervals.

        Take, for example, the following two periods:
        >>> period1_start = date(2024, 1, 1)
        >>> period1_end = date(2024, 1, 10)
        >>> period1 = DatePeriod(start=period1_start, end=period1_end)
        >>> period2_start = date(2024, 1, 5)
        >>> period2_end = date(2024, 1, 15)
        >>> period2 = DatePeriod(start=period2_start, end=period2_end)
        >>> period1
        DatePeriod(start=datetime.date(2024, 1, 1), end=datetime.date(2024, 1, 10))
        >>> period2
        DatePeriod(start=datetime.date(2024, 1, 5), end=datetime.date(2024, 1, 15))

        On a timeline, the two periods can be illustrated as:
        2024-01-01      Period 1                2024-01-10
            |=========================================|
                               |============================================|
                         2024-01-05             Period 2              2024-01-15

        From the point of view of Period 1, the disconnect between the two periods is between the 1st and the 5th;
        however, from the point of view of Period 2, the disconnect between them is between the 10th and the 15th.

        Therefore, if you want to obtain the amount of time when the periods do NOT overlap as relative to Period 1,
        you should use:
        >>> period1.get_disconnect(period2)
        DatePeriod(start=datetime.date(2024, 1, 1), end=datetime.date(2024, 1, 5))

        But if you want to obtain the same as relative to Period 2 instead:
        >>> period2.get_disconnect(period1)
        DatePeriod(start=datetime.date(2024, 1, 10), end=datetime.date(2024, 1, 15))
        """
        if not isinstance(other, DatePeriod) and not isinstance(other, DatetimePeriod):
            raise TypeError(f"Cannot perform temporal operations with instances of type '{type(other)}'")
        if self.overlapped_by(other):
            end_date = other.start if isinstance(other, DatePeriod) else other.start.date()
            return DatePeriod(start=self.start, end=end_date)
        elif self.overlaps_with(other):
            start_date = other.end if isinstance(other, DatePeriod) else other.end.date()
            return DatePeriod(start=start_date, end=self.end)


class DatetimePeriod(Period):

    def __init__(self,
                 start: datetime,
                 end: datetime,
                 ):
        if not isinstance(start, datetime):
            raise ValueError(f"Provided value '{start}' for parameter 'start' is not an instance of "
                             f"datetime.datetime")
        if not isinstance(end, datetime):
            raise ValueError(f"Provided value '{end}' for parameter 'end' is not an instance of "
                             f"datetime.datetime")
        super().__init__(start, end)

    def _time_repeats(self,
                      _t: time | TimePeriod) -> bool:
        """ Internal method that checks if the provided time or TimePeriod will repeat within the duration of this
         period.

         for datetime.time objects:
         In all cases where this period is equal to or longer than 2 days (48h), this method will return True;
         For 1 day long periods (24h) or shorter, if the time is within the start and end of this period,
         it will return True;

         for periods.TimePeriod objects:
         In all cases where this period is longer than 2 days (over 72h), it will return True;
         In cases where the period is 2 days long (up to 72h), it will only return True if the TimePeriod does NOT start
         AND end before and after, respectively, this period.
         In cases of 1 day long (up to 48h) periods, it will only return True if the TimePeriod does not either start
         before this period, or end after it.

         It is important to remember that this method only checks FULL repetition, meaning this:
           0800               1700           Midnight        0800                   1700
            /========================================================================/ <- This Period
               /======/                                            /======/            <- TimePeriod
             0900    1200                                        0900    1200

         Cases of partially overlapping, but not fully, will return Fase:
           0800               1700           Midnight        0800                   1700
            /========================================================================/         <- This Period
         /=============================/                   /=============================/     <- TimePeriod
        0700                         2000                0700                           2000

         """
        if isinstance(_t, time):
            if self.duration.days >= 2:
                return True
            elif self.duration.days == 1:
                if self.start.time() <= _t <= self.end.time():
                    return True
        if isinstance(_t, TimePeriod):
            if self.duration.days > 2:
                # No situation in which the period won't repeat when the period is over 2 days long
                return True
            if self.duration.days == 2:
                # If the period is 2 days long, the TimePeriod must start before it and end after it in order not to
                # repeat, otherwise, it will repeat
                if not _t.start < self.start.time() or not self.end.time() < _t.end:
                    return True
            elif self.duration.days == 1:
                # If the period is (at least) 1 day long, it must either start before it or end after it not to repeat
                if self.start.time() <= _t.start and _t.end <= self.end.time():
                    # The other period starts at the same time or later and ends either before or at the same time as
                    # this one - it will exist twice within it
                    return True
        return False

    def __eq__(self, other):
        """ Equality can be determined between this class and any other of the Period classes, since this class contains
        the most complete information of a period in time.

        For instances of TimePeriod, equality will be measured in terms of hours;
        For instances of DatePeriod, equality will be measured in terms of dates;
        For instances of this class, equality will be measured for both.

        This method does not account for overlaps between the start and end times and/or dates of the periods, to get
        this functionality, look at the following methods:
            overlaps_with
            overlapped_by
            get_overlap
            get_disconnect
        """
        if isinstance(other, DatetimePeriod):
            return (self.start == other.start
                    and self.end == other.end)
        if isinstance(other, DatePeriod):
            return (self.start.date() == other.start
                    and self.end.date() == other.end)
        if isinstance(other, TimePeriod):
            return (self.start.time() == other.start
                    and self.end.time() == other.end)
        return False

    def __contains__(self, item):
        """ Membership test can be done with instances of this class, the DatePeriod and TimePeriod classes,
        datetime.datetime and datetime.date objects; When membership test is done for a period, it assumes that the
        request is to check if the tested period exists WITHIN the temporal borders of this period, that is to say,
        whether the start and end time and/or date of the other period are after and before, respectively, of the same
        of this period.

        2024-01-01 08:00 Your period: 2024-03-01 08:00
            |==================================|
                    |=============|     <---- The period you are testing
        2024-02-01 08:00   2024-02-15 08:00

        If you have an instance of this period, for example:
        >>> start = datetime(2024, 1, 1, 8, 0)  # 0800, 1st of Jan 2024
        >>> end = datetime(2024, 3, 1, 8, 0)  # 0800, 1st of Mar 2024
        >>> quarter = DatetimePeriod(start=start, end=end)

        and then another DatetimePeriod:
        >>> pto_start = datetime(2024, 2, 1, 8, 0)  # 0800, 1st of Feb 2024
        >>> pto_end = datetime(2024, 2, 15, 8, 0)  # 0800, 15th of Feb 2024
        >>> pto = DatetimePeriod(start=pto_start, end=pto_end)

        Then you can check if the pto period is within your quarter period:
        >>> pto in quarter

        For more in-depth comparisons and functionality, see:
            overlaps_with
            overlapped_by
            get_overlap
            get_disconnect

        Raises:
            TimeAmbiguityError - raised if the duration of this period is longer than a day and either a TimePeriod is
                tested, or an instance of datetime.time that falls within the start and end of this period. Also see:
                <url to doc>
                for more information.
        """
        if isinstance(item, DatetimePeriod):
            return self.start <= item.start and item.end <= self.end
        if isinstance(item, DatePeriod):
            return self.start.date() <= item.start and item.end <= self.end.date()
        if isinstance(item, TimePeriod):
            if self._time_repeats(item):
                raise TimeAmbiguityError(f"The provided TimePeriod '{item}' exist within this DatetimePeriod "
                                         f"('{self}') more than once. For more information on this error, "
                                         f"see https://github.com/dimitarOnGithub/temporals/wiki/Misc")
            if self.duration.days == 1:
                if item.start < self.start.time():
                    if item.end <= self.end.time():
                        # Period starts before this once but ends before or at the same time as this once, hence
                        # existing only once
                        return True
                    else:
                        # Period never fully exists within this one as it starts before it and ends after it
                        return False
                if item.start >= self.start.time():
                    if self.end.time() < item.end:
                        # Starts equal or later but ends later too - existing only once
                        return True
            return self.start.time() <= item.start and item.end <= self.end.time()
        if isinstance(item, datetime):
            return self.start <= item <= self.end
        if isinstance(item, date):
            return self.start.date() <= item <= self.end.date()
        if isinstance(item, time):
            if self._time_repeats(item):
                raise TimeAmbiguityError(f"The provided unit of time ('{item}') exist within this DatetimePeriod "
                                         f"('{self}')  more than once. For more information on this error, "
                                         f"see https://github.com/dimitarOnGithub/temporals/wiki/Misc")
            if self.duration.days == 1:
                return True
            return self.start.time() <= item <= self.end.time()
        return False

    def overlaps_with(self,
                      other: Union['TimePeriod', 'DatePeriod', 'DatetimePeriod']
                      ) -> bool:
        """ Test if this period overlaps with another period that has begun before this one. This check will evaluate
        as True in the following scenario:
                    2024-02-01 0800  This period:   2024-03-01 1700
                            |==================================|
                     |============================|   <------ The other period
            2024-02-01 0600             2024-02-01 1300

        >>> this_start = datetime(2024, 2, 1, 8, 0)  # 0800, 2nd of Feb 2024
        >>> this_end = datetime(2024, 2, 1, 17, 0)  # 1700, 2nd of Feb 2024
        >>> other_start = datetime(2024, 2, 1, 6, 0)  # 0600, 2nd of Feb 2024
        >>> other_end = datetime(2024, 2, 1, 13, 0)  # 1300, 2nd of Feb 2024
        >>> this_period = DatetimePeriod(start=this_start, end=this_end)
        >>> other_period = DatetimePeriod(start=other_start, end=other_end)
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
        if isinstance(other, TimePeriod):
            if self._time_repeats(other):
                raise TimeAmbiguityError(f"The provided TimePeriod '{other}' exist within this DatetimePeriod "
                                         f"('{self}') more than once. For more information on this error, "
                                         f"see https://github.com/dimitarOnGithub/temporals/wiki/Misc")
            if self.start.date() < self.end.date():
                # Day stretches overnight - the start time must be before the start of this period but also after the
                # end of it
                if other.start < self.start.time() and other.start < self.end.time():
                    raise TimeAmbiguityError(f"The provided TimePeriod ('{other}') is ambiguous compared to this "
                                             f"DatetimePeriod ('{self}'); it's overlapped by (starts before) this "
                                             f"period on {self.start.date().isoformat()} but this period continues "
                                             f"until after it's start on {self.end.date().isoformat()}")
                else:
                    if not other.end < self.start.time():
                        return other.start <= self.start.time()
            else:
                if not other.end < self.start.time():
                    return other.start < self.start.time() and other.end < self.end.time()
        if isinstance(other, DatePeriod):
            if not other.end < self.start.date():
                return other.start < self.start.date() and other.end < self.end.date()
        if isinstance(other, DatetimePeriod):
            if not other.end < self.start:
                return other.start < self.start and other.end < self.end
        return False

    def overlapped_by(self,
                      other: Union['TimePeriod', 'DatePeriod', 'DatetimePeriod']
                      ) -> bool:
        """ Test if this period is overlapped by the other period. This check will evaluate True in the following
        scenario:
        2024-01-01 0800   This period:  2024-01-01 1700
                |==================================|
                        |=====================================|   <------ The other period
                2024-01-01 1200                    2024-01-01 2300

        >>> this_start = datetime(2024, 1, 1, 8, 0)  # 0800, 1st of Jan 2024
        >>> this_end = datetime(2024, 1, 1, 17, 0)  # 1700, 1st of Jan 2024
        >>> other_start = datetime(2024, 1, 1, 12, 0)  # 1200, 1st of Jan 2024
        >>> other_end = datetime(2024, 1, 1, 23, 0)  # 2300, 1st of Jan 2024
        >>> this_period = DatePeriod(start=this_start, end=this_end)
        >>> other_period = DatePeriod(start=other_start, end=other_end)
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
        if isinstance(other, TimePeriod):
            if self._time_repeats(other):
                raise TimeAmbiguityError(f"The provided TimePeriod '{other}' exist within this DatetimePeriod "
                                         f"('{self}') more than once. For more information on this error, "
                                         f"see https://github.com/dimitarOnGithub/temporals/wiki/Misc")
            if self.start.date() < self.end.date():
                # Day stretches overnight - the start time must be after the start of this period but also after the
                # end of it
                if self.start.time() < other.start and self.end.time() < other.end:
                    raise TimeAmbiguityError(f"The provided TimePeriod ('{other}') is ambiguous compared to this "
                                             f"DatetimePeriod ('{self}'); it overlaps with (starts after) this "
                                             f"period on {self.start.date().isoformat()} but this period continues "
                                             f"until after it's start on {self.end.date().isoformat()}")
                else:
                    if not self.end.time() < other.start:
                        return self.start.time() <= other.start
            else:
                if not self.end.time() < other.start:
                    return self.start.time() < other.start and self.end.time() < other.end
        if isinstance(other, DatePeriod):
            if not self.end.date() < other.start:
                return self.start.date() < other.start and self.end.date() < other.end
        if isinstance(other, DatetimePeriod):
            if not self.end < other.start:
                return self.start < other.start and self.end < other.end
        return False

    def get_overlap(self,
                    other: Union['TimePeriod', 'DatePeriod', 'DatetimePeriod']
                    ) -> Union['TimePeriod', 'DatePeriod', 'DatetimePeriod', None]:
        """ Method returns the overlapping interval between the two periods as a new period instance. Returned object
        will be an instance of the class that's being tested.

        >>> period1_start = datetime(2024, 1, 1, 8, 0, 0)
        >>> period1_end = datetime(2024, 1, 1, 12, 0, 0)
        >>> period1 = DatetimePeriod(start=period1_start, end=period1_end)
        >>> period2_start = time(10, 0, 0)
        >>> period2_end = time(13, 0, 0)
        >>> period2 = TimePeriod(start=period2_start, end=period2_end)
        >>> period1
        DatetimePeriod(start=datetime.datetime(2024, 1, 1, 8, 0), end=datetime.datetime(2024, 1, 1, 12, 0))
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
        if (not isinstance(other, TimePeriod)
                and not isinstance(other, DatePeriod)
                and not isinstance(other, DatetimePeriod)):
            raise TypeError(f"Cannot perform temporal operations with instances of type '{type(other)}'")
        period_to_use = None
        _start = None
        _end = None
        if self.overlaps_with(other) or self.overlapped_by(other):
            if isinstance(other, TimePeriod):
                period_to_use = TimePeriod
                _start = self.start.time() if self.overlaps_with(other) else other.start
                _end = other.end if self.overlaps_with(other) else self.end.time()
            elif isinstance(other, DatePeriod):
                period_to_use = DatePeriod
                _start = self.start.date() if self.overlaps_with(other) else other.start
                _end = other.end if self.overlaps_with(other) else self.end.date()
            else:
                period_to_use = DatetimePeriod
                _start = self.start if self.overlaps_with(other) else other.start
                _end = other.end if self.overlaps_with(other) else self.end
        return period_to_use(start=_start, end=_end)

    def get_disconnect(self,
                       other: Union['TimePeriod', 'DatePeriod', 'DatetimePeriod']
                       ) -> Union['TimePeriod', 'DatePeriod', 'DatetimePeriod', None]:
        """ Method returns the disconnect interval from the point of view of the invoking period. This means the time
        disconnect from the start of this period until the start of the period to which this period is being compared
        to. Since the span of time is relative to each of the two periods, this method will always return different
        intervals.

        Take, for example, the following two periods:
        >>> period1_start = datetime(2024, 1, 1, 8, 0, 0)
        >>> period1_end = datetime(2024, 1, 1, 12, 0, 0)
        >>> period1 = DatetimePeriod(start=period1_start, end=period1_end)
        >>> period2_start = datetime(2024, 1, 1, 10, 0, 0)
        >>> period2_end = datetime(2024, 1, 1, 13, 0, 0)
        >>> period2 = DatetimePeriod(start=period2_start, end=period2_end)
        >>> period1
        DatetimePeriod(start=datetime.datetime(2024, 1, 1, 8, 0), end=datetime.datetime(2024, 1, 1, 12, 0))
        >>> period2
        DatetimePeriod(start=datetime.datetime(2024, 1, 1, 10, 0), end=datetime.datetime(2024, 1, 1, 13, 0))

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
        DatetimePeriod(start=datetime.datetime(2024, 1, 1, 8, 0), end=datetime.datetime(2024, 1, 1, 10, 0))

        But if you want to obtain the same as relative to Period 2 instead:
        >>> period2.get_disconnect(period1)
        DatetimePeriod(start=datetime.datetime(2024, 1, 1, 12, 0), end=datetime.datetime(2024, 1, 1, 13, 0))
        """
        if (not isinstance(other, TimePeriod)
                and not isinstance(other, DatePeriod)
                and not isinstance(other, DatetimePeriod)):
            raise TypeError(f"Cannot perform temporal operations with instances of type '{type(other)}'")
        period_to_use = None
        _start = None
        _end = None
        if isinstance(other, TimePeriod):
            period_to_use = TimePeriod
            if self.overlapped_by(other):
                _start = self.start.time()
                _end = other.start
            elif self.overlaps_with(other):
                _start = other.end
                _end = self.end.time()
        elif isinstance(other, DatePeriod):
            period_to_use = DatePeriod
            if self.overlapped_by(other):
                _start = self.start.date()
                _end = other.start
            elif self.overlaps_with(other):
                _start = other.end
                _end = self.end.date()
        else:
            period_to_use = DatetimePeriod
            if self.overlapped_by(other):
                _start = self.start
                _end = other.start
            elif self.overlaps_with(other):
                _start = other.end
                _end = self.end
        if period_to_use and _start and _end:
            return period_to_use(start=_start, end=_end)


class Duration:

    def __init__(self,
                 *,
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
        self.seconds: int = 0
        self.minutes: int = 0
        self.hours: int = 0
        self.days: int = 0
        self.weeks: int = 0
        self.months: int = 0
        self.years: int = 0
        self._calculate_period()

    def _calculate_period(self):
        self.seconds: int = int(self.timedelta.total_seconds())
        self.minutes: int = self.seconds // 60
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
        """ This method returns the duration in an ISO-8601 (https://en.wikipedia.org/wiki/ISO_8601#Durations) format.
        Optional parameter `fold` can be set to False (True by default) to display even the empty elements of the
        duration.

        TODO: There must be a more intelligent way to do that
        """
        _rep = "P"
        if self.years or not fold:
            _rep = f"{_rep}{self.years}Y"
        if self.months or not fold:
            _rep = f"{_rep}{self.months}M"
        if self.weeks or not fold:
            _rep = f"{_rep}{self.weeks}W"
        if self.days or not fold:
            _rep = f"{_rep}{self.days}D"
        # From now on, it's time elements, so we must append "T"
        if (self.hours or self.minutes or self.seconds) or not fold:
            _rep = f"{_rep}T"
            if self.hours or not fold:
                _rep = f"{_rep}{self.hours}H"
            if self.minutes or not fold:
                _rep = f"{_rep}{self.minutes}M"
            if self.seconds or not fold:
                _rep = f"{_rep}{self.seconds}S"
        return _rep

    def format(self, pattern: str):
        """ Offers a way to format the representation of this Duration similar to datetime's strftime. In the _map
        dictionary below you can see which characters will be replaced by which values."""
        _map = {
            '%Y': self.years,
            '%m': self.months,
            '%W': self.weeks,
            '%d': self.days,
            '%H': self.hours,
            '%M': self.minutes,
            '%S': self.seconds
        }
        for key, value in _map.items():
            if key in pattern:
                pattern = pattern.replace(key, str(value))
        return pattern
