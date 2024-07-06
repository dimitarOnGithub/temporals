from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo


class Period:

    def __init__(self,
                 start: date | datetime,
                 end: date | datetime,
                 zone_overwrite: ZoneInfo | str = None,
                 inherit_zone: bool = False
                 ):
        self.start = start
        self.end = end
        self.duration = None


class TimePeriod(Period):

    def __init__(self, start, end, **kwargs):
        super().__init__(start, end)


class DatePeriod(Period):

    def __init__(self, start: date, end: date, **kwargs):
        super().__init__(start, end)


class DatetimePeriod(Period):

    def __init__(self, start, end, **kwargs):
        super().__init__(start, end)


class Duration:

    def __init__(self,
                 start,
                 end,
                 **kwargs):
        pass
