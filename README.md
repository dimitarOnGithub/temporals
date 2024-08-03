# Temporals

The goal of this library is to provide a minimalistic, out-of-the-box utility on top of the Python's 
`datetime` in regards to working with time and date, or both, periods.

> :warning: As it currently stands (assume the latest release), the library has no out of the box support
> for "aware" datetime objects. All the calculations are done by the Python `datetime` library.

## Quickstart

### Installation

You can either download the latest package from this repository or via pip:

`pip install temporals`

### Periods

The library offers access to three different types of periods:

- **TimePeriod**

    The `TimePeriod` class allows you to define a period using `datetime.time`, and as such, is limited
to just the 24 hours within a day.

- **DatePeriod**

    The `DatePeriod` class allows you to define a period using `datetime.date` and work with any dates
within its bounds.

- **DatetimePeriod**

    This is the most complete implementation of both periods above as it contains both a date, and a time, 
defined using `datetime.datetime`.

### Documentation

In-depth documentation available on the Wiki page of the repository - https://github.com/dimitarOnGithub/temporals/wiki

### Examples

As mentioned above, you might find use for the different periods in different situations, let's look at
the following `TimePeriod` example:
```python
from datetime import time
from temporals import TimePeriod

workday = TimePeriod(start=time(8, 0), end=time(18, 0))
# Do you have an important call scheduled?
client_call = time(13, 0)
print(client_call in workday)  # True

# Or maybe you have an appointment and you want to see if it overlaps with your work hours?
appointment = TimePeriod(start=time(17, 30), end=time(18, 15))
appointment.overlaps_with(workday)  # True

# Let's see what's the overlap like, so you can plan accordingly
overlap = appointment.get_overlap(workday)  # get_overlap returns a TimePeriod
print(overlap)  # 17:30:00/18:00:00
```

---

Let's do something less day-to-day like, with this `DatePeriod`:
```python
from datetime import date
from temporals import DatePeriod

time_off = DatePeriod(start=date(2024, 8, 1), end=date(2024, 8, 14))
# All roads lead to Rome
italy_visit = DatePeriod(start=date(2024, 8, 3), end=date(2024, 8, 10))

# I hope you have a good... how long again?
print(italy_visit.duration)  # P0Y0M1W0DT0H0M0S
# Wow, that sure is a mouthful, can we get it simplified?
print(italy_visit.duration.isoformat(fold=True))  # 'P1W'
```

---

Sometimes, we need both date and time to properly describe a period in time and this is the purpose
`DatetimePeriod` serves
```python
from datetime import datetime
from temporals import DatetimePeriod

takeoff = datetime(2024, 8, 2, 22, 11, 34)  # 22:11:34, 2nd of Aug 2024
landing = datetime(2024, 8, 3, 4, 55, 3)  # 04:55:03, 3rd of Aug 2024

flight = DatetimePeriod(start=takeoff, end=landing)
print(flight)  
# 2024-08-02T22:11:34/2024-08-03T04:55:03

# This is a PITA to read, why not try something nicer
print(flight.duration.isoformat())
# PT6H43M29S

# "Stop. Enhance. Give me a hard copy right there."
pattern = "%Hh%Mm"
formatted_time = flight.duration.format(pattern)
sentence = f"The flight lasted around {formatted_time}"
print(sentence)
# The flight lasted around 6h43m
```
