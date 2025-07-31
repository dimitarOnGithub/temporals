from abc import ABC, abstractmethod


class AbstractDuration(ABC):
    """ A representation of the duration of each period """

    @property
    @abstractmethod
    def seconds(self) -> int:
        """ Return the seconds in the Duration; not the total duration to seconds! """

    @property
    @abstractmethod
    def minutes(self) -> int:
        """ Return the minutes in the Duration; not the total duration to minutes! """

    @property
    @abstractmethod
    def hours(self) -> int:
        """ Return the hours in the Duration; not the total duration to hours! """

    @property
    @abstractmethod
    def days(self) -> int:
        """ Return the days in the Duration; not the total duration to days! """

    @property
    @abstractmethod
    def months(self) -> int:
        """ Return the months in the Duration; not the total duration to months! """

    @property
    @abstractmethod
    def years(self) -> int:
        """ Return the years in the Duration; not the total duration to years! """

    @abstractmethod
    def isoformat(self, fold: bool) -> str:
        """ Implementing methods must return a string value that conforms to the ISO-8601 standard:
        https://en.wikipedia.org/wiki/ISO_8601#Durations

        Additionally, the `fold` parameter may be predefined/provided, when True, zero values should be omitted
        """

    @abstractmethod
    def format(self, pattern):
        """ A helper method that allows the user to provide a specific pattern for the output """
