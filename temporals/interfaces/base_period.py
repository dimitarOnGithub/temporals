from abc import ABC, abstractmethod
from .period_duration import AbstractDuration


class AbstractPeriod(ABC):
    """ Implementations of this class must provide logic for the 'equal' comparison, via __eq__ method, as well as the
    membership test operators (is, is not) via __contains__ """

    @property
    @abstractmethod
    def start(self):
        """ Ensure instance remains read-only. Implementing a setter must return a new object """

    @property
    @abstractmethod
    def end(self):
        """ Ensure instance remains read-only. Implementing a setter must return a new object """

    @property
    @abstractmethod
    def duration(self) -> 'AbstractDuration':
        """ Returns the Duration of this period; using a property ensures that the value cannot be overridden by default
        """

    def __repr__(self):
        return f"{self.__class__.__name__}(start={self.start.__repr__()}, end={self.end.__repr__()})"

    @abstractmethod
    def __str__(self):
        """ Implementation must conform to ISO-8601 """

    @abstractmethod
    def __eq__(self, other):
        """ Different implementations will contain different logic for determining whether this instance is equal to the
        provided one, one important thing to note is:

        This method does not account for overlaps between the start and end times of the periods, to get this
        functionality, look at the following methods:
            overlaps_with
            overlapped_by
            get_overlap
            get_disconnect
        """

    @abstractmethod
    def __contains__(self, item):
        """ Different implementations will contain different logic for determining whether this instance "contains" the
        provided one.

        When membership test is done for a period, it assumes that the request is to check if
        the tested period exists WITHIN the temporal borders of this period, that is to say, whether the start and
        end times of the other period are after and before, respectively, of the same of this period, for example:

        0800       Period 1:          1700
        |==================================|
             1200 |=============| 1300
                     Period 2

        Period 2 exists completely within Period 1, so if you perform a membership test, True will be returned:
        >> period2 in period1 ? -> True
        """

    @abstractmethod
    def is_before(self, other) -> bool:
        """ Test if this period ends before the provided `other` value:

        1000 This period:   1400
        |====================|
                                | 1500
                            Point in time

        This period ends before the `other`, thus True is returned
        """

    @abstractmethod
    def is_after(self, other) -> bool:
        """ Test if this period starts after the provided `other` value:

                        1000       This period:          1700
                        |==================================|
                    | <- `other`, an example time
                  0900
        This period starts after the `other`, thus True is returned
        """

    @abstractmethod
    def get_interim(self, other):
        """ Returns the interval between the start/end of this period and the provided other (another period, time,
        date or datetime).

        This method is intended to be used when the provided `other` does not exist within and does not overlap (or is
        being overlapped) by this period.

        For example, in the case of a point of in time:
        1000       This period:          1700
        |==================================|
                                                | 2000
                                         Point in time

        The returned TimePeriod will be from 1700 to 2000
        """

    @abstractmethod
    def overlaps_with(self, other) -> bool:
        """ Test if this period overlaps with another period that has begun before this one:
                       1000       This period:          1700
                        |==================================|
             0800 |=============| 1300
                         ^ The other period
        The period that has begun first is considered the "main" period, even if it finishes before the end of this
        period, since it occupies an earlier point in time. Therefore, the current period (this instance), which has
        begun at a later point in time, is considered to be overlapping with the "main" one
        """

    @abstractmethod
    def overlapped_by(self, other) -> bool:
        """ Test if this period is overlapped by the other period. This check will evaluate True in the following
        scenario:
           1000       This period:          1700
            |==================================|
                                1500 |=============| 1800
                                            ^ The other period
        Since this period has begun first, it is considered the "main" one, and all other periods that begin after this
        one, are overlapping it.
        """

    @abstractmethod
    def get_overlap(self, other):
        """ Method returns the overlapping interval between the two periods as a new period; different implementations
        will be accepting and returning different values.
        On a timeline, the periods can be illustrated as:
           0800              Period 1                1200
            |=========================================|
                                        |============================|
                                       1000       Period 2          1500

        A membership test would return False:
        >> period2 in period1? False
        because period2 is not fully contained within period1; However, testing overlaps would return True:
        >> period1.overlapped_by(period2)? True
        and the opposite:
        >> period2.overlaps_with(period1)? True

        Therefore, the `get_overlap` method should obtain the precise length of the overlapping interval:
        >> period1.get_overlap(period2) -> 1000 to 1200
        And since the overlap is always the same, regardless of the observer, the opposite action would have the same
        result:
        >> period2.get_overlap(period1) -> 1000 to 1200
        """

    @abstractmethod
    def get_disconnect(self, other):
        """ Method returns the disconnect interval from the point of view of the invoking period. This means the time
        disconnect from the start of this period until the start of the period to which this period is being compared
        to. Since the span of time is relative to each of the two periods, this method will always return different
        intervals.

        Take, for example, the following two periods::
           0800              Period 1                1200
            |=========================================|
                               |============================|
                              1000       Period 2          1300

        From the point of view of Period 1, the disconnect between the two periods is between the time 0800 and 1000,
        because Period 1 has begun when Period 2 was still inexistent, and in the same manner, from the point of view
        of Period 2, the disconnect between them is between the time 1200 and 1300, because Period 1 ceases to exist at
        1200 while Period 2 continues until 1300.

        Therefore, if you want to obtain the amount of time when the periods do NOT overlap as relative to Period 1,
        you should use:
        >> period1.get_disconnect(period2) -> 0800 to 1000
        But if you want to obtain the same as relative to Period 2 instead:
        >> period2.get_disconnect(period1) -> 1200 to 1300
        """
