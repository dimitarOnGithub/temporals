# Temporals

The goal of this library is to provide a minimalistic, out-of-the-box utility on top of the Python's 
`datetime` in regards to working with time and date, or both, periods.

## Installation

You can either download the latest package from this repository or via pip:

`pip install temporals`

## Documentation

Full documentation is available in the [wiki](https://github.com/dimitarOnGithub/temporals/wiki) of this repository.

## Quickstart

The library offers 4 types of periods - time, date, wall clock and absolute. For the sake of example, we'll keep it simple here and just define a time period that we'll call our work day:
```python
from datetime import time
from temporals.pydatetime import TimePeriod

workday = TimePeriod(start=time(8, 0), end=time(18, 0))
# You can use a membership check to see if a point in time or another period exists within one that you've already defined
lunch= time(12, 0)
print(lunch in workday)  # True
# Or you can see if two periods overlap
dentist_slot = TimePeriod(start=time(17, 30), end=time(18, 30))
print(dentist_slot.overlaps_with(workday)) # True
# You can also get the precise amount of overlap/disconnect
# both of these return a new TimePeriod object :)
print(dentist_slot.get_overlap(workday)) # 17:30:00/18:00:00
print(dentist_slot.get_disconnect(workday)) # 18:00:00/18:30:00
```

If 24h long day isn't what you're looking for, the `DatePeriod` will fill the need for having periods with no specific time info:
```python
from datetime import date
from temporals.pydatetime import DatePeriod

vacation = DatePeriod(start=date(2025, 8, 1), end=date(2025, 8, 14))
# Each period has a `.duration` attribute which returns an instance of the Duration class:
vacation.duration # Duration(total_seconds=1123200, years=0, months=0, days=13, hours=0, minutes=0, seconds=0)
# A simpler way would be to just call the isoformat method of the Duration class:
print(vacation.duration.isoformat(fold=True)) # 'P13D'
```

For the greatest precision, you could use one of the two classes - `WallClockPeriod` or `AbsolutePeriod`.
The difference between the two is, as you can probably guess, that the duration of the WallClockPeriod's class will be as if tracked by
looking at a clock on the wall; the same for the AbsolutePeriod's class, however, will measure the absolute amount of time thath as passed, 
irrelevant of the time shifts that may happen throughout its duration.
```python
from datetime import time, date
from temporals.pydatetime import TimePeriod, DatePeriod

vacation = DatePeriod(start=date(2025, 8, 1), end=date(2025, 8, 14))
# Let's be a bit more specific with our vacation
flight_duration = TimePeriod(start=time(7, 55), end=time(14, 24))
# The start of the time period above will be matched as a start to the DatePeriod and the same will be done for the end
italy_visit = vacation.to_wallclock(specific_time=flight_duration)
# WallClockPeriod(start=datetime.datetime(2025, 8, 1, 7, 55), end=datetime.datetime(2025, 8, 14, 14, 24))
# Our duration looks a bit more complete now:
print(italy_visit.duration.isoformat(fold=True)) # 'P13DT6H29M'
# that, however, doesn't necessarily make it readable, so let's update it:
sentence: str = f"Our total time spent travelling to and from, as well as our stay there, Italy, took %d days, %H hours and %M minutes"
print(italy_visit.duration.format(sentence))
# Our total time spent travelling to and from, as well as our stay there, Italy, took 13 days, 6 hours and 29 minutes
```
