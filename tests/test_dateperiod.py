import pytest
from datetime import time, date, datetime
from temporals.periods import DatePeriod, DatetimePeriod, TimePeriod


class TestDatePeriod:

    def test_constructor_valid(self):
        # Valid objects
        self.start = date(2024, 1, 1)
        self.end = date(2024, 1, 1)
        self.period = DatePeriod(start=self.start, end=self.end)
        assert isinstance(self.period, DatePeriod)

    def test_constructor_invalid(self):
        # Time
        self.start = time(13, 1, 1)
        self.end = time(14, 1, 2)
        with pytest.raises(ValueError):
            DatePeriod(start=self.start, end=self.end)

        # Datetime
        self.start = datetime(2024, 1, 1, 8, 0, 0)
        self.end = datetime(2024, 1, 1, 10, 0, 0)
        with pytest.raises(ValueError):
            DatePeriod(start=self.start, end=self.end)

    def test_dateperiod_eq(self):
        self.start = date(2024, 1, 1)
        self.end = date(2024, 1, 30)
        self.period1 = DatePeriod(start=self.start, end=self.end)
        self.period2 = DatePeriod(start=self.start, end=self.end)
        assert self.period1 == self.period2

        self.different_end = date(2024, 1, 10)
        self.period2 = DatePeriod(start=self.start, end=self.different_end)
        assert self.period1 != self.period2

    def test_datetimeperiod_eq(self):
        self.start = date(2024, 1, 1)
        self.end = date(2024, 1, 30)
        self.period = DatePeriod(start=self.start, end=self.end)
        self.start_dt = datetime(2024, 1, 1, 8, 0, 0)
        self.end_dt = datetime(2024, 1, 30, 10, 0, 0)
        self.period_dt = DatetimePeriod(start=self.start_dt, end=self.end_dt)
        assert self.period == self.period_dt

    def test_invalid_eq(self):
        self.random_date = date(2024, 2, 1)
        self.start = date(2024, 1, 1)
        self.end = date(2024, 1, 30)
        self.period = DatePeriod(start=self.start, end=self.end)
        assert self.random_date != self.period

    def test_membership(self):
        self.random_date = date(2024, 1, 15)
        self.start = date(2024, 1, 1)
        self.end = date(2024, 1, 30)
        self.period = DatePeriod(start=self.start, end=self.end)
        assert self.random_date in self.period

        self.start = date(2024, 1, 5)
        self.end = date(2024, 1, 10)
        self.inner_period = DatePeriod(start=self.start, end=self.end)
        assert self.inner_period in self.period

        self.start = date(2024, 1, 1)
        self.end = date(2024, 1, 30)
        self.eq_period = DatePeriod(start=self.start, end=self.end)
        assert self.eq_period in self.period

        self.random_dt = datetime(2024, 1, 1, 10, 0, 0)
        assert self.random_dt in self.period

        self.start_dt = datetime(2024, 1, 1, 8, 30, 0)
        self.end_dt = datetime(2024, 1, 2, 9, 0, 0)
        self.period_dt = DatetimePeriod(start=self.start_dt, end=self.end_dt)
        assert self.period_dt in self.period

    def test_is_before(self):
        self.start = date(2024, 1, 1)
        self.end = date(2024, 1, 10)
        self.period = DatePeriod(start=self.start, end=self.end)
        assert self.period.is_before(date(2024, 1, 11)) is True
        assert self.period.is_before(date(2024, 1, 10)) is False
        assert self.period.is_before(datetime(2024, 1, 11, 8, 0)) is True
        assert self.period.is_before(datetime(2024, 1, 10, 8, 0)) is False

        self.other_start = date(2024, 1, 11)
        self.other_end = date(2024, 1, 30)
        self.other_period = DatePeriod(start=self.other_start, end=self.other_end)
        assert self.period.is_before(self.other_period) is True

        self.other_start = date(2024, 1, 10)
        self.other_end = date(2024, 1, 30)
        self.other_period = DatePeriod(start=self.other_start, end=self.other_end)
        assert self.period.is_before(self.other_period) is False

        self.other_start = datetime(2024, 1, 10, 8, 0)
        self.other_end = datetime(2024, 1, 12, 8, 0)
        self.other_period = DatetimePeriod(start=self.other_start, end=self.other_end)
        assert self.period.is_before(self.other_period) is False

        self.other_start = datetime(2024, 1, 11, 8, 0)
        self.other_end = datetime(2024, 1, 12, 8, 0)
        self.other_period = DatetimePeriod(start=self.other_start, end=self.other_end)
        assert self.period.is_before(self.other_period) is True

    def test_is_after(self):
        self.start = date(2024, 1, 10)
        self.end = date(2024, 1, 20)
        self.period = DatePeriod(start=self.start, end=self.end)
        assert self.period.is_after(date(2024, 1, 10)) is False
        assert self.period.is_after(date(2024, 1, 9)) is True
        assert self.period.is_after(datetime(2024, 1, 10, 8, 0)) is False
        assert self.period.is_after(datetime(2024, 1, 9, 8, 0)) is True

        self.other_start = date(2024, 1, 1)
        self.other_end = date(2024, 1, 10)
        self.other_period = DatePeriod(start=self.other_start, end=self.other_end)
        assert self.period.is_after(self.other_period) is False

        self.other_start = date(2024, 1, 1)
        self.other_end = date(2024, 1, 5)
        self.other_period = DatePeriod(start=self.other_start, end=self.other_end)
        assert self.period.is_after(self.other_period) is True

        self.other_start = datetime(2024, 1, 1, 8, 0)
        self.other_end = datetime(2024, 1, 10, 8, 0)
        self.other_period = DatetimePeriod(start=self.other_start, end=self.other_end)
        assert self.period.is_after(self.other_period) is False

        self.other_start = datetime(2024, 1, 1, 8, 0)
        self.other_end = datetime(2024, 1, 9, 8, 0)
        self.other_period = DatetimePeriod(start=self.other_start, end=self.other_end)
        assert self.period.is_after(self.other_period) is True

    def test_combine(self):
        self.start = date(2024, 1, 10)
        self.end = date(2024, 1, 20)
        self.period = DatePeriod(start=self.start, end=self.end)
        assert self.period.combine(time(8, 0)) == DatetimePeriod(
            start=datetime(2024, 1, 10, 8, 0),
            end=datetime(2024, 1, 20, 8, 0)
        )

        self.start = date(2024, 1, 10)
        self.end = date(2024, 1, 20)
        self.period = DatePeriod(start=self.start, end=self.end)
        self.other_start = time(8, 0)
        self.other_end = time(12, 0)
        self.other_period = TimePeriod(start=self.other_start, end=self.other_end)
        assert self.period.combine(self.other_period) == DatetimePeriod(
            start=datetime(2024, 1, 10, 8, 0),
            end=datetime(2024, 1, 20, 12, 0)
        )

    def test_get_interim(self):
        self.start = date(2024, 1, 10)
        self.end = date(2024, 1, 20)
        self.period = DatePeriod(start=self.start, end=self.end)
        assert (self.period.get_interim(
            date(2024, 1, 1)
        ) == DatePeriod(date(2024, 1, 1), date(2024, 1, 10)))
        assert (self.period.get_interim(
            date(2024, 1, 30)
        ) == DatePeriod(date(2024, 1, 20), date(2024, 1, 30)))

        self.other_start = date(2024, 1, 1)
        self.other_end = date(2024, 1, 5)
        self.other_period = DatePeriod(start=self.other_start, end=self.other_end)
        assert (self.period.get_interim(self.other_period) == DatePeriod(date(2024, 1, 5),
                                                                         date(2024, 1, 10)))

        self.other_start = date(2024, 1, 25)
        self.other_end = date(2024, 1, 30)
        self.other_period = DatePeriod(start=self.other_start, end=self.other_end)
        assert (self.period.get_interim(self.other_period) == DatePeriod(date(2024, 1, 20),
                                                                         date(2024, 1, 25)))

    def test_overlaps(self):
        """
        2024-01-01 Period 1   2024-01-10
            |=====================|
                                |===================|
                            2024-01-09 Period 2  2024-01-30

            Period 1 is overlapped by Period 2
            Period 2 overlaps Period 1
            Period 1 does not overlap Period 2
            Period 2 is not overlapped by Period 1
        """
        self.start = date(2024, 1, 1)
        self.end = date(2024, 1, 10)
        self.period = DatePeriod(start=self.start, end=self.end)

        self.other_start = date(2024, 1, 9)
        self.other_end = date(2024, 1, 30)
        self.other_period = DatePeriod(start=self.other_start, end=self.other_end)
        assert self.period.overlapped_by(self.other_period) is True
        assert self.other_period.overlaps_with(self.period) is True
        assert self.period.overlaps_with(self.other_period) is False
        assert self.other_period.overlapped_by(self.period) is False

    def test_disconnects(self):
        """
           2024-01-01 Period 1 2024-01-10
            |=====================|
                                |===================|
                            2024-01-09 Period 2  2024-01-30

            Period 1 disconnect - 2024-01-01 to 2024-01-09
            Period 2 disconnect - 2024-01-10 to 2024-01-30

        """
        self.start = date(2024, 1, 1)
        self.end = date(2024, 1, 10)
        self.period = DatePeriod(start=self.start, end=self.end)

        self.other_start = date(2024, 1, 9)
        self.other_end = date(2024, 1, 30)
        self.other_period = DatePeriod(start=self.other_start, end=self.other_end)

        self.first_disconnect = self.period.get_disconnect(self.other_period)
        assert self.first_disconnect.start == date(2024, 1, 1)
        assert self.first_disconnect.end == date(2024, 1, 9)

        self.second_disconnect = self.other_period.get_disconnect(self.period)
        assert self.second_disconnect.start == date(2024, 1, 10)
        assert self.second_disconnect.end == date(2024, 1, 30)

        # Non overlapping periods
        self.other_start = date(2024, 1, 15)
        self.other_end = date(2024, 1, 30)
        self.other_period = DatePeriod(start=self.other_start, end=self.other_end)

        self.first_disconnect = self.period.get_disconnect(self.other_period)
        assert self.first_disconnect is None

        self.second_disconnect = self.other_period.get_disconnect(self.period)
        assert self.second_disconnect is None
