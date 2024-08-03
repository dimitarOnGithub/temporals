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

        # TimePeriod that starts before it and ends after it
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
        # TimePeriod that starts before it but also ends before it
        self.period1 = TimePeriod(start=time(7, 0), end=time(10, 0))
        assert self.period._time_repeats(self.period1) is True
        # TimePeriod that starts after it but also ends after it
        self.period1 = TimePeriod(start=time(9, 0), end=time(12, 0))
        assert self.period._time_repeats(self.period1) is True
        # TimePeriod that starts and ends within it
        self.period1 = TimePeriod(start=time(9, 0), end=time(10, 0))
        assert self.period._time_repeats(self.period1) is True
        # TimePeriod that has start time and end time after this period - not repeating
        self.period1 = TimePeriod(start=time(7, 0), end=time(12, 0))
        assert self.period._time_repeats(self.period1) is False

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
        # Same day period
        self.start = datetime(2024, 1, 1, 8, 0)
        self.end = datetime(2024, 1, 1, 12, 0)
        self.period = DatetimePeriod(start=self.start, end=self.end)

        # Time test
        self.time = time(17, 0)
        print(self.time in self.period)
        assert self.time not in self.period

        # Date test
        self.date = date(2024, 1, 2)
        assert self.date not in self.period

        # Datetime test
        self.datetime = datetime(2024, 1, 1, 13, 0)
        assert self.datetime not in self.period

        # Time period test - overlapping
        self.time_period = TimePeriod(
            start=time(9, 0),
            end=time(14, 0)
        )
        assert self.time_period not in self.period

    def test_overlaps_time(self):
        """
            Same day:

           0800 Period 1         1200
            |=====================|
                                |===================|
                              1100 Period 2        1700

            Period 1 is overlapped by Period 2
            Period 2 overlaps Period 1
            Period 1 does not overlap Period 2
            Period 2 is not overlapped by Period 1
        """
        self.start = datetime(2024, 1, 1, 8, 0)
        self.end = datetime(2024, 1, 1, 12, 0)
        self.period = DatetimePeriod(start=self.start, end=self.end)

        self.other_start = time(10, 0)
        self.other_end = time(14, 0)
        self.other_period = TimePeriod(start=self.other_start, end=self.other_end)

        assert self.period.overlapped_by(self.other_period) is True
        assert self.other_period.overlaps_with(self.period) is True
        assert self.period.overlaps_with(self.other_period) is False
        assert self.other_period.overlapped_by(self.period) is False

    def test_overlaps_date(self):
        """
        2024-01-01 0800        Period 1         2024-01-03 1200
            |=========================================|
                                |===================================================|
                            2024-01-02                   Period 2              2024-01-04

            Period 1 is overlapped by Period 2
            Period 2 overlaps Period 1
            Period 1 does not overlap Period 2
            Period 2 is not overlapped by Period 1
        """
        self.start = datetime(2024, 1, 1, 8, 0)
        self.end = datetime(2024, 1, 3, 12, 0)
        self.period = DatetimePeriod(start=self.start, end=self.end)

        self.other_start = date(2024, 1, 2)
        self.other_end = date(2024, 1, 4)
        self.other_period = DatePeriod(start=self.other_start, end=self.other_end)

        assert self.period.overlapped_by(self.other_period) is True
        assert self.other_period.overlaps_with(self.period) is True
        assert self.period.overlaps_with(self.other_period) is False
        assert self.other_period.overlapped_by(self.period) is False

    def test_overlaps_datetime(self):
        """
            Same day:

           0800 Period 1         1200
            |=====================|
                                |===================|
                              1100 Period 2        1700

            Period 1 is overlapped by Period 2
            Period 2 overlaps Period 1
            Period 1 does not overlap Period 2
            Period 2 is not overlapped by Period 1
        """
        self.start = datetime(2024, 1, 1, 8, 0)
        self.end = datetime(2024, 1, 1, 12, 0)
        self.period = DatetimePeriod(start=self.start, end=self.end)

        self.other_start = datetime(2024, 1, 1, 11, 0)
        self.other_end = datetime(2024, 1, 1, 17, 0)
        self.other_period = DatetimePeriod(start=self.other_start, end=self.other_end)
        assert self.period.overlapped_by(self.other_period) is True
        assert self.other_period.overlaps_with(self.period) is True
        assert self.period.overlaps_with(self.other_period) is False
        assert self.other_period.overlapped_by(self.period) is False

        """
            Different day:

            2024-01-01 0800 Period 1        2024-02-01 1200
                    |==============================|
                                        |===============================|
                                    2024-01-15 0800 Period 2  2024-03-01 1200

            Period 1 is overlapped by Period 2
            Period 2 overlaps Period 1
            Period 1 does not overlap Period 2
            Period 2 is not overlapped by Period 1
        """
        self.start = datetime(2024, 1, 1, 8, 0)
        self.end = datetime(2024, 2, 1, 12, 0)
        self.period = DatetimePeriod(start=self.start, end=self.end)

        self.other_start = datetime(2024, 1, 15, 11, 0)
        self.other_end = datetime(2024, 3, 1, 12, 0)
        self.other_period = DatetimePeriod(start=self.other_start, end=self.other_end)
        assert self.period.overlapped_by(self.other_period) is True
        assert self.other_period.overlaps_with(self.period) is True
        assert self.period.overlaps_with(self.other_period) is False
        assert self.other_period.overlapped_by(self.period) is False

    def test_ambiguity_time(self):
        """ All tests below must raise a TimeAmbiguityError """

        # Membership ambiguity
        """ 2 day long period
                2024-01-01 0800                                         2024-01-02 1200
                    /==========================================================/
                       /=======/                                       /======/
                    1000     1200                                   1000     1200
        """
        self.start = datetime(2024, 1, 1, 8, 0)
        self.end = datetime(2024, 1, 2, 12, 0)
        self.period = DatetimePeriod(start=self.start, end=self.end)

        self.time = time(9, 0)
        with pytest.raises(TimeAmbiguityError):
            self.time in self.period

        """ 1 day long period 
                2024-01-01 0800                                         2024-01-02 1200
                    /==========================================================/
                       /=======/                                       /======/
                    1000     1200                                   1000     1200
        """
        self.start = datetime(2024, 1, 1, 8, 0)
        self.end = datetime(2024, 1, 2, 12, 0)
        self.period = DatetimePeriod(start=self.start, end=self.end)

        self.other_start = time(10, 0)
        self.other_end = time(12, 0)
        self.other_period = TimePeriod(start=self.other_start, end=self.other_end)

        with pytest.raises(TimeAmbiguityError):
            self.other_period in self.period

        # Overlaps with ambiguity
        """ 2 days long period 
                2024-01-01 0800                                         2024-01-02 1200
                    /==========================================================/
                        /=========/                                        /=========/
                    1000       1400                                      1000      1400
        """
        self.start = datetime(2024, 1, 1, 8, 0)
        self.end = datetime(2024, 1, 3, 12, 0)
        self.period = DatetimePeriod(start=self.start, end=self.end)

        self.other_start = time(10, 0)
        self.other_end = time(14, 0)
        self.other_period = TimePeriod(start=self.other_start, end=self.other_end)

        with pytest.raises(TimeAmbiguityError):
            self.period.overlaps_with(self.other_period)

        self.other_start = time(6, 0)
        self.other_end = time(14, 0)
        self.other_period = TimePeriod(start=self.other_start, end=self.other_end)

        with pytest.raises(TimeAmbiguityError):
            self.period.overlaps_with(self.other_period)

        """ Overnight period 
                2024-01-01 1000              Midnight                   2024-01-02 0800
                    /==========================================================/
                /=======/                                                   /======/
              0700    1200                                                0700    1200
        """
        self.start = datetime(2024, 1, 1, 10, 0)
        self.end = datetime(2024, 1, 2, 8, 0)
        self.period = DatetimePeriod(start=self.start, end=self.end)

        self.other_start = time(7, 0)
        self.other_end = time(12, 0)
        self.other_period = TimePeriod(start=self.other_start, end=self.other_end)

        with pytest.raises(TimeAmbiguityError):
            self.period.overlaps_with(self.other_period)

        # Overlapped by ambiguity
        """ 2 days long period 
                2024-01-01 0800                                         2024-01-02 1200
                    /==========================================================/
                        /=========/                                        /=========/
                      1000       1400                                    1000      1400
        """
        self.start = datetime(2024, 1, 1, 8, 0)
        self.end = datetime(2024, 1, 2, 12, 0)
        self.period = DatetimePeriod(start=self.start, end=self.end)

        self.other_start = time(10, 0)
        self.other_end = time(14, 0)
        self.other_period = TimePeriod(start=self.other_start, end=self.other_end)

        with pytest.raises(TimeAmbiguityError):
            self.period.overlapped_by(self.other_period)

        """ Overnight period 
                2024-01-01 0600                Midnight               2024-01-02 1000
                    /==========================================================/
                        /=========/                                        /=========/
                      1000       1400                                    1000      1400
        """
        self.start = datetime(2024, 1, 1, 6, 0)
        self.end = datetime(2024, 1, 2, 10, 0)
        self.period = DatetimePeriod(start=self.start, end=self.end)

        self.other_start = time(10, 0)
        self.other_end = time(14, 0)
        self.other_period = TimePeriod(start=self.other_start, end=self.other_end)

        with pytest.raises(TimeAmbiguityError):
            self.period.overlapped_by(self.other_period)

    def test_get_overlap(self):
        # Same day period
        self.start = datetime(2024, 1, 1, 8, 0)
        self.end = datetime(2024, 1, 1, 12, 0)
        self.period = DatetimePeriod(start=self.start, end=self.end)

        # Time period test
        self.time_period = TimePeriod(
            start=time(9, 0),
            end=time(13, 0)
        )
        self.overlap = self.period.get_overlap(self.time_period)
        assert self.overlap == TimePeriod(start=time(9, 0), end=time(12, 0))
        # TODO: re-do this once the get_overlap method for TimePeriod has been refactored
        self.other_overlap = self.time_period.get_overlap(self.period)
        assert self.other_overlap == TimePeriod(start=time(9, 0), end=time(12, 0))

        # 2 day period
        self.start = datetime(2024, 1, 1, 8, 0)
        self.end = datetime(2024, 1, 3, 12, 0)
        self.period = DatetimePeriod(start=self.start, end=self.end)

        # Date period test
        self.date_period = DatePeriod(
            start=date(2024, 1, 2),
            end=date(2024, 1, 4)
        )
        self.overlap = self.period.get_overlap(self.date_period)
        assert self.overlap == DatePeriod(start=date(2024, 1, 2),
                                          end=date(2024, 1, 3))

        # Datetime period test
        self.start = datetime(2024, 1, 1, 8, 0)
        self.end = datetime(2024, 1, 3, 12, 0)
        self.period = DatetimePeriod(start=self.start, end=self.end)

        self.dt_period = DatetimePeriod(
            start=datetime(2024, 1, 2, 10, 0),
            end=datetime(2024, 1, 4, 8, 0)
        )
        self.overlap = self.period.get_overlap(self.date_period)
        assert self.overlap == DatetimePeriod(
            start=datetime(2024, 1, 2, 10, 0),
            end=datetime(2024, 1, 3, 12, 0)
        )

    def test_get_disconnect(self):
        # Same day period
        self.start = datetime(2024, 1, 1, 8, 0)
        self.end = datetime(2024, 1, 1, 12, 0)
        self.period = DatetimePeriod(start=self.start, end=self.end)

        # Time period test
        self.time_period = TimePeriod(
            start=time(9, 0),
            end=time(13, 0)
        )
        self.dc = self.period.get_disconnect(self.time_period)
        assert self.dc == TimePeriod(start=time(8, 0), end=time(9, 0))
        self.other_dc = self.time_period.get_disconnect(self.period)
        assert self.other_dc == TimePeriod(start=time(12, 0), end=time(13, 0))

        # 2 day period
        self.start = datetime(2024, 1, 1, 8, 0)
        self.end = datetime(2024, 1, 3, 12, 0)
        self.period = DatetimePeriod(start=self.start, end=self.end)

        # Date period test
        self.date_period = DatePeriod(
            start=date(2024, 1, 2),
            end=date(2024, 1, 4)
        )
        self.dc = self.period.get_disconnect(self.date_period)
        assert self.dc == DatePeriod(start=date(2024, 1, 1),
                                     end=date(2024, 1, 2))
        self.other_dc = self.date_period.get_disconnect(self.period)
        assert self.other_dc == DatePeriod(start=date(2024, 1, 3),
                                           end=date(2024, 1, 4))

        # Datetime period test
        self.start = datetime(2024, 1, 1, 8, 0)
        self.end = datetime(2024, 1, 3, 12, 0)
        self.period = DatetimePeriod(start=self.start, end=self.end)

        self.dt_period = DatetimePeriod(
            start=datetime(2024, 1, 2, 10, 0),
            end=datetime(2024, 1, 4, 8, 0)
        )
        self.dc = self.period.get_disconnect(self.date_period)
        assert self.dc == DatetimePeriod(
            start=datetime(2024, 1, 1, 8, 0),
            end=datetime(2024, 1, 2, 10, 0)
        )
        self.other_dc = self.dt_period.get_disconnect(self.period)
        assert self.other_dc == DatetimePeriod(
            start=datetime(2024, 1, 3, 12, 0),
            end=datetime(2024, 1, 4, 8, 0)
        )

        # Non overlapping periods
        # Same day period
        self.start = datetime(2024, 1, 1, 8, 0)
        self.end = datetime(2024, 1, 1, 12, 0)
        self.period = DatetimePeriod(start=self.start, end=self.end)

        # Time period test
        self.time_period = TimePeriod(
            start=time(13, 0),
            end=time(14, 0)
        )
        self.dc = self.period.get_disconnect(self.time_period)
        assert self.dc is None
        self.other_dc = self.time_period.get_disconnect(self.period)
        assert self.other_dc is None

        # Date period test
        self.start = datetime(2024, 1, 1, 8, 0)
        self.end = datetime(2024, 1, 5, 12, 0)
        self.period = DatetimePeriod(start=self.start, end=self.end)

        self.date_period = DatePeriod(
            start=date(2024, 1, 10),
            end=date(2024, 1, 15)
        )
        self.dc = self.period.get_disconnect(self.date_period)
        assert self.dc is None
        self.other_dc = self.date_period.get_disconnect(self.period)
        assert self.other_dc is None

        # Datetime period test
        self.dt_period = DatetimePeriod(
            start=datetime(2023, 12, 10, 10, 0),
            end=datetime(2023, 12, 15, 8, 0)
        )
        self.dc = self.period.get_disconnect(self.dt_period)
        assert self.dc is None
        self.other_dc = self.dt_period.get_disconnect(self.period)
        assert self.other_dc is None
