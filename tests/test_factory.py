import pytest
from datetime import time, date
from temporals import PeriodFactory
from temporals import TimePeriod, DatePeriod, DatetimePeriod


class TestFactory:

    def test_invalid_params(self):
        self.factory = PeriodFactory
        with pytest.raises(ValueError):
            self.factory('foo', 'bar')
            self.factory('foo', 'bar', force_datetime=True)

    def test_time_period_object_creation(self):
        self.factory = PeriodFactory
        a = self.factory("13:00", "15:00")
        assert isinstance(a, TimePeriod)

    def test_date_period_creation(self):
        self.factory = PeriodFactory
        a = self.factory("2024-11-01", "2024-11-15")
        assert isinstance(a, DatePeriod)

    def test_datetime_period_creation(self):
        self.factory = PeriodFactory
        a = self.factory("2024-11-01 13:00", "2024-11-01 15:00")
        assert isinstance(a, DatetimePeriod)

    def test_force_creation_time(self):
        self.factory = PeriodFactory
        a = self.factory(
            time(10, 0),
            time(12, 0),
            force_datetime=True)
        assert isinstance(a, DatetimePeriod)

    def test_force_creation_date(self):
        self.factory = PeriodFactory
        a = self.factory(
            date(2024, 1, 1),
            date(2024, 1, 10),
            force_datetime=True)
        assert isinstance(a, DatetimePeriod)
