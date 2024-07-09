import pytest
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

