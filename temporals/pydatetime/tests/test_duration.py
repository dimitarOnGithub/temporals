import pytest
from datetime import time, date, datetime
from zoneinfo import ZoneInfo
from temporals.exceptions import NonexistentTimeError
from temporals.pydatetime.periods import TimePeriod, DatePeriod, WallClockPeriod, AbsolutePeriod

# TODO: Fix reference to private attribute _total
class TestDuration:

    def test_time(self):
        period = TimePeriod(start=time(10, 0, 0), end=time(12, 0, 0))
        assert period.duration.hours == 2
        assert period.duration._total == 7200

        period = TimePeriod(start=time(10, 35, 15), end=time(12, 0, 0))
        assert period.duration.hours == 1
        assert period.duration.minutes == 24
        assert period.duration.seconds == 45
        assert period.duration._total == 5085

        period = TimePeriod(start=time(10, 58, 59), end=time(12, 0, 0))
        assert period.duration.hours == 1
        assert period.duration.minutes == 1
        assert period.duration.seconds == 1

    def test_date(self):
        period = DatePeriod(start=date(2025, 1, 1), end=date(2025, 1, 2))
        assert period.duration.days == 1

        period = DatePeriod(start=date(2025, 1, 1), end=date(2025, 2, 1))
        assert period.duration.months == 1
        assert period.duration.days == 0

        period = DatePeriod(start=date(2025, 2, 1), end=date(2025, 3, 1))
        assert period.duration.months == 1
        assert period.duration.days == 0

        period = DatePeriod(start=date(2025, 1, 1), end=date(2025, 3, 1))
        assert period.duration.months == 2
        assert period.duration.days == 0
        # Total is less than the leap date test below because February has fewer days
        assert period.duration._total == 5097600


    def test_leap_date(self):
        period = DatePeriod(start=date(2024, 1, 1), end=date(2024, 3, 1))
        assert period.duration.months == 2
        assert period.duration.days == 0
        # Total is more than the non-leap date test above because February has more days
        assert period.duration._total == 5184000

    def test_wallclock(self):
        period = WallClockPeriod(start=datetime(2025, 1, 1, 10, 0, 0),
                                 end=datetime(2025, 1, 2, 12, 15, 30))
        assert period.duration.days == 1
        assert period.duration.hours == 2
        assert period.duration.minutes == 15
        assert period.duration.seconds == 30

        period = WallClockPeriod(start=datetime(2025, 1, 1, 12, 15, 30),
                                 end=datetime(2025, 1, 2, 10, 0, 0))
        assert period.duration.days == 0
        assert period.duration.hours == 21
        assert period.duration.minutes == 44
        assert period.duration.seconds == 30

    def test_wallclock_timeshift(self):
        period = WallClockPeriod(start=datetime(2025, 3, 30, 1, 0, tzinfo=ZoneInfo(key='Europe/Paris')),
                                 end=datetime(2025, 3, 30, 4, 0, tzinfo=ZoneInfo(key='Europe/Paris')))
        assert period.duration.days == 0
        assert period.duration.hours == 3
        assert period.duration.minutes == 0
        assert period.duration.seconds == 0

        # removing an hour
        period = WallClockPeriod(start=datetime(2025, 10, 26, 2, 0, tzinfo=ZoneInfo(key='Europe/Paris')),
                                end=datetime(2025, 10, 26, 4, 0, tzinfo=ZoneInfo(key='Europe/Paris')))
        assert period.duration.hours == 2

    def test_absolute_notz(self):
        period = AbsolutePeriod(start=datetime(2025, 1, 1, 10, 0, 0),
                                 end=datetime(2025, 1, 2, 12, 15, 30))
        assert period.duration.days == 1
        assert period.duration.hours == 2
        assert period.duration.minutes == 15
        assert period.duration.seconds == 30

        period = AbsolutePeriod(start=datetime(2025, 7, 1, 10, 0, 0),
                                end=datetime(2025, 7, 2, 12, 15, 30))
        assert period.duration.days == 1
        assert period.duration.hours == 2
        assert period.duration.minutes == 15
        assert period.duration.seconds == 30

    def test_absolute_tz(self):
        period = AbsolutePeriod(start=datetime(2025, 1, 1, 10, 0, 0, tzinfo=ZoneInfo(key='Europe/Paris')),
                                end=datetime(2025, 1, 2, 12, 15, 30, tzinfo=ZoneInfo(key='Europe/Paris')))
        assert period.duration.days == 1
        assert period.duration.hours == 2
        assert period.duration.minutes == 15
        assert period.duration.seconds == 30

        period = AbsolutePeriod(start=datetime(2025, 7, 1, 10, 0, 0, tzinfo=ZoneInfo(key='Europe/Paris')),
                                end=datetime(2025, 7, 2, 12, 15, 30, tzinfo=ZoneInfo(key='Europe/Paris')))
        assert period.duration.days == 1
        assert period.duration.hours == 2
        assert period.duration.minutes == 15
        assert period.duration.seconds == 30

        period = AbsolutePeriod(start=datetime(2025, 4, 6, 1, 0, 0, tzinfo=ZoneInfo(key='Australia/Lord_Howe')),
                                end=datetime(2025, 4, 6, 2, 0, 0, tzinfo=ZoneInfo(key='Australia/Lord_Howe'), fold=1))
        assert period.duration.days == 0
        assert period.duration.hours == 1
        assert period.duration.minutes == 30

        period = AbsolutePeriod(start=datetime(2025, 10, 5, 1, 0, 0, tzinfo=ZoneInfo(key='Australia/Lord_Howe')),
                                end=datetime(2025, 10, 5, 3, 0, 0, tzinfo=ZoneInfo(key='Australia/Lord_Howe')))
        assert period.duration.days == 0
        assert period.duration.hours == 1
        assert period.duration.minutes == 30

    def test_absolute_nonexisting(self):
        # 2 AM in the Paris timezone does not exist since the clock shifts forward to 3 AM
        with pytest.raises(NonexistentTimeError):
            AbsolutePeriod(start=datetime(2025, 3, 30, 2, 0, tzinfo=ZoneInfo(key='Europe/Paris')),
                           end=datetime(2025, 3, 30, 3, 0, tzinfo=ZoneInfo(key='Europe/Paris')))

    def test_absolute_timeshift(self):
        # shift forward by 1 hour
        period = AbsolutePeriod(start=datetime(2025, 3, 30, 1, 0, tzinfo=ZoneInfo(key='Europe/Paris')),
                                end=datetime(2025, 3, 30, 4, 0, tzinfo=ZoneInfo(key='Europe/Paris')))
        assert period.duration.hours == 2

        # shift backwards by 1 hour
        period = AbsolutePeriod(start=datetime(2025, 10, 26, 2, 0, tzinfo=ZoneInfo(key='Europe/Paris')),
                                end=datetime(2025, 10, 26, 4, 0, tzinfo=ZoneInfo(key='Europe/Paris')))
        assert period.duration.hours == 3

    def test_absolute_overflow(self):
        # shift forward by 1 hour
        period = AbsolutePeriod(start=datetime(2025, 3, 30, 1, 0, tzinfo=ZoneInfo(key='Europe/Paris')),
                                end=datetime(2025, 3, 31, 2, 0, tzinfo=ZoneInfo(key='Europe/Paris')))
        assert period.duration.days == 1
        assert period.duration.hours == 0

        # shift backwards by 1 hour - repeated time
        period = AbsolutePeriod(start=datetime(2025, 10, 26, 2, 0, tzinfo=ZoneInfo(key='Europe/Paris')),
                                end=datetime(2025, 10, 27, 2, 0, tzinfo=ZoneInfo(key='Europe/Paris')))
        assert period.duration.days == 1
        assert period.duration.hours == 1

        # shift backwards by 1 hour - non-repeated time
        period = AbsolutePeriod(start=datetime(2025, 10, 26, 2, 0, tzinfo=ZoneInfo(key='Europe/Paris'), fold=1),
                                end=datetime(2025, 10, 27, 2, 0, tzinfo=ZoneInfo(key='Europe/Paris')))
        assert period.duration.days == 1
        assert period.duration.hours == 0
