import pytest
from datetime import time, date, datetime
from temporals.periods import TimePeriod, DatePeriod, DatetimePeriod
from temporals.exceptions import TimeAmbiguityError


class TestDatetimePeriod:

    def test_constructor_valid(self):
        # Valid objects
        self.start = datetime(2024, 1, 1, 8, 0)
        self.end = datetime(2024, 1, 1, 12, 0)
        self.period = DatetimePeriod(start=self.start, end=self.end)
        assert isinstance(self.period, DatetimePeriod)

    def test_constructor_invalid(self):
        # Time
        self.start = time(13, 1, 1)
        self.end = time(14, 1, 2)
        with pytest.raises(ValueError):
            DatetimePeriod(start=self.start, end=self.end)

        # Date
        self.start = date(2024, 1, 1)
        self.end = date(2024, 1, 1)
        with pytest.raises(ValueError):
            DatetimePeriod(start=self.start, end=self.end)

    def test_nonrepeating_time(self):
        """ This tests the internal _time_repeats method """
        self.start = datetime(2024, 1, 1, 8, 0)
        self.end = datetime(2024, 1, 2, 12, 0)
        self.period = DatetimePeriod(start=self.start, end=self.end)

        self.time = time(7, 0)
        assert self.period._time_repeats(self.time) is False
        self.time = time(13, 0)
        assert self.period._time_repeats(self.time) is False

        self.period1 = TimePeriod(start=time(7, 0), end=time(10, 0))
        assert self.period._time_repeats(self.period1) is False
        self.period1 = TimePeriod(start=time(9, 0), end=time(13, 0))
        assert self.period._time_repeats(self.period1) is False

        # 48h period
        self.start = datetime(2024, 1, 1, 8, 0)
        self.end = datetime(2024, 1, 3, 11, 0)
        self.period = DatetimePeriod(start=self.start, end=self.end)

        # TimePeriod that starts before it
        self.period1 = TimePeriod(start=time(7, 0), end=time(10, 0))
        assert self.period._time_repeats(self.period1) is False

        # TimePeriod that ends after it
        self.period1 = TimePeriod(start=time(7, 0), end=time(12, 0))
        assert self.period._time_repeats(self.period1) is False

    def test_repeating_time(self):
        """ This tests the internal _time_repeat method """
        self.start = datetime(2024, 1, 1, 8, 0)
        self.end = datetime(2024, 1, 2, 12, 0)
        self.period = DatetimePeriod(start=self.start, end=self.end)

        self.time = time(10, 0)
        assert self.period._time_repeats(self.time) is True
        self.period1 = TimePeriod(start=time(9, 0), end=time(11, 0))
        assert self.period._time_repeats(self.period1) is True

        # More than 24h period
        self.start = datetime(2024, 1, 1, 8, 0)
        self.end = datetime(2024, 1, 3, 11, 0)
        self.period = DatetimePeriod(start=self.start, end=self.end)

        self.time = time(7, 0)
        assert self.period._time_repeats(self.time) is True
        # TimePeriod that starts and ends within it
        self.period1 = TimePeriod(start=time(9, 0), end=time(10, 0))
        assert self.period._time_repeats(self.period1) is True

    def test_timeperiod_eq(self):
        self.start = datetime(2024, 1, 1, 8, 0)
        self.end = datetime(2024, 1, 1, 12, 0)
        self.period1 = TimePeriod(start=self.start.time(), end=self.end.time())
        self.period2 = DatetimePeriod(start=self.start, end=self.end)
        assert self.period1 == self.period2

    def test_dateperiod_eq(self):
        self.start = datetime(2024, 1, 1, 8, 0)
        self.end = datetime(2024, 1, 1, 12, 0)
        self.period1 = DatePeriod(start=self.start.date(), end=self.end.date())
        self.period2 = DatetimePeriod(start=self.start, end=self.end)
        assert self.period1 == self.period2

        self.different_end = date(2024, 1, 10)
        self.period2 = DatePeriod(start=self.start.date(), end=self.different_end)
        assert self.period1 != self.period2

    def test_datetimeperiod_eq(self):
        self.start = datetime(2024, 1, 1, 8, 0)
        self.end = datetime(2024, 1, 1, 12, 0)
        self.period = DatetimePeriod(start=self.start, end=self.end)
        self.start_dt = datetime(2024, 1, 1, 8, 0)
        self.end_dt = datetime(2024, 1, 1, 12, 0)
        self.period_dt = DatetimePeriod(start=self.start_dt, end=self.end_dt)
        assert self.period == self.period_dt

    def test_invalid_eq(self):
        self.random_dt = datetime(2024, 1, 1, 8, 0)
        self.start = datetime(2024, 1, 1, 8, 0)
        self.end = datetime(2024, 1, 1, 12, 0)
        self.period = DatetimePeriod(start=self.start, end=self.end)
        assert self.random_dt != self.period

    def test_valid_membership(self):
        # Same day period
        self.start = datetime(2024, 1, 1, 8, 0)
        self.end = datetime(2024, 1, 1, 12, 0)
        self.period = DatetimePeriod(start=self.start, end=self.end)

        # Time test
        self.time = time(10, 0)
        assert self.time in self.period

        # Date test
        self.date = date(2024, 1, 1)
        assert self.date in self.period

        # Datetime test
        self.datetime = datetime(2024, 1, 1, 12, 0)
        assert self.datetime in self.period

        # Time period test
        self.time_period = TimePeriod(
            start=time(9, 0),
            end=time(11, 0)
        )
        assert self.time_period in self.period

        # DatetimePeriod test
        self.dt_period = DatetimePeriod(
            start=datetime(2024, 1, 1, 9, 0),
            end=datetime(2024, 1, 1, 11, 0)
        )
        assert self.dt_period in self.period

        # 24h period
        self.start = datetime(2024, 1, 1, 8, 0)
        self.end = datetime(2024, 1, 2, 12, 0)
        self.period = DatetimePeriod(start=self.start, end=self.end)

        # Time test
        self.time = time(7, 0)
        assert self.time in self.period
        self.time = time(13, 0)
        assert self.time in self.period

        # Date test
        self.date = date(2024, 1, 2)
        assert self.date in self.period

        # Time period test
        self.time_period = TimePeriod(
            start=time(7, 0),
            end=time(11, 0)
        )
        assert self.time_period in self.period

        self.time_period = TimePeriod(
            start=time(9, 0),
            end=time(13, 0)
        )
        assert self.time_period in self.period

    def test_invalid_membership(self):
        pass
