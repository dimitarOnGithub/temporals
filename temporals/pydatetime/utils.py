from datetime import datetime
from zoneinfo import ZoneInfo
from temporals.exceptions import NonexistentTimeError


def check_existence(value: datetime) -> datetime:
    """ Utility function that verifies that the provided datetime object is not ambiguous (inexistent when clock goes
    forward).

    Important to note, in the case of repeating time, an error will not be raised - it's up to you to decide whether the
    provided time is intended as-is.

    Kudos go to @ariebovenberg (https://github.com/ariebovenberg) and his article on common pitfalls with the datetime
    library - https://dev.arie.bovenberg.net/blog/python-datetime-pitfalls/

    Raises:
        NonexistentTimeError
    """
    if value.tzinfo is None:
        return value
    # If a time does not exist due to the clock shifting forward, switching the timezone to UTC and back to the original
    # one, will result in a time shift as well; evaluate if the modified object equals the original one
    orig_tz = value.tzinfo
    shifted = value.astimezone(ZoneInfo("UTC")).astimezone(orig_tz)
    if value != shifted:
        raise NonexistentTimeError(value, orig_tz)
    return value
