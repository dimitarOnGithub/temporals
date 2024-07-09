import pytest
from sys import version_info
from datetime import time, date, datetime
from temporals.utils import get_datetime, _test_pattern, _test_defaults, _convert_to_type, convert_to_datetime


class TestUtils:

    def test_get_datetime_invalid(self):
        with pytest.raises(ValueError):
            get_datetime("foo")
            get_datetime("bar", force_datetime=True)

    def test_get_datetime_returns(self):
        self._time = time(15, 30, 11)
        assert isinstance(get_datetime(self._time), time)
        self._date = date.today()
        assert isinstance(get_datetime(self._date), date)
        self._datetime = datetime.now()
        assert isinstance(get_datetime(self._datetime), datetime)

    def test_get_datetime_force(self):
        self._time = time(15, 30, 11)
        assert isinstance(get_datetime(self._time, force_datetime=True), datetime)
        self._date = date.today()
        assert isinstance(get_datetime(self._date, force_datetime=True), datetime)
        self._datetime = datetime.now()
        assert isinstance(get_datetime(self._datetime, force_datetime=True), datetime)

    def test_time_patterns(self):
        self.valid_time = '15:30:11'
        self.valid_time_p = '%H:%M:%S'
        assert isinstance(_test_pattern(self.valid_time, self.valid_time_p), datetime)

    def test_date_patterns(self):
        self.valid_date = '2024-01-01'
        self.valid_date_p = '%Y-%m-%d'
        assert isinstance(_test_pattern(self.valid_date, self.valid_date_p), datetime)

    def test_datetime_patterns(self):
        self.valid_datetime = '2024-01-01T15:30:11'
        self.valid_datetime_p = '%Y-%m-%dT%H:%M:%S'
        assert isinstance(_test_pattern(self.valid_datetime, self.valid_datetime_p), datetime)

    def test_invalid_patterns(self):
        self.invalid = '01:15 PM'
        self.invalid_p = '%H:%M'
        assert _test_pattern(self.invalid, self.invalid_p) is None

    def test_time_defaults(self):
        # Time
        self.valid_time = '15:30:11'
        assert isinstance(_test_defaults(self.valid_time), time)
        if version_info.minor > 10:
            # Only available starting 3.11 onwards
            self.valid_time_tz = '15:30:11-0700'
            assert isinstance(_test_defaults(self.valid_time_tz), time)
        self.invalid_time = '01:15 PM'
        assert _test_defaults(self.invalid_time) is None

    def test_date_defaults(self):
        # Date
        self.valid_date = '2024-01-01'
        assert isinstance(_test_defaults(self.valid_date), date)
        self.valid_date_ord = 739075
        assert isinstance(_test_defaults(self.valid_date_ord), date)
        self.valid_date_ord_str = '739075'
        assert isinstance(_test_defaults(self.valid_date_ord_str), date)
        self.invalid_date = '24-01-01'
        assert _test_defaults(self.invalid_date) is None

    def test_datetime_defaults(self):
        # Datetime
        self.valid_datetime = '2024-01-01T15:30:11'
        assert isinstance(_test_defaults(self.valid_datetime), datetime)
        self.valid_datetime_ts = 1720447072.169697
        assert isinstance(_test_defaults(self.valid_datetime_ts), datetime)
        self.valid_datetime_ts_str = '1720447072.169697'
        assert isinstance(_test_defaults(self.valid_datetime_ts_str), datetime)

    def test_type_conversion(self):
        assert isinstance(_convert_to_type(12345, str), str)
        assert isinstance(_convert_to_type('12345', int), int)
        assert isinstance(_convert_to_type('12345.67890', float), float)
        assert _convert_to_type('foobar', float) is None
        assert _convert_to_type('foobar', int) is None

    def test_datetime_conversion(self):
        self.dt = datetime.fromisoformat('2024-01-01T15:30:11')
        assert isinstance(convert_to_datetime(self.dt), datetime)
        self.date = date(2024, 1, 1)
        assert isinstance(convert_to_datetime(self.date), datetime)
        self.time = time(15, 30, 11)
        assert isinstance(convert_to_datetime(self.time), datetime)
        try:
            from datetime import UTC
            self.time_tz = time(15, 30, 11, tzinfo=UTC)
        except ImportError:
            self.time_tz = datetime.utcnow()
        assert isinstance(convert_to_datetime(self.time_tz), datetime)
        assert convert_to_datetime(self.time_tz) is not None
