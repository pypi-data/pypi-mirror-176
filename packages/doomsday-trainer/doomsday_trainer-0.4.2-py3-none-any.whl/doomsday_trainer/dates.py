"""Date handling."""
import random
from datetime import datetime


class DoomsdayRule:
    """An representation of the application of the Doomsday rule to a specific date."""

    def __init__(self, doomsdate):
        """Initialize object."""
        self.doomsdate = doomsdate

    def short_year(self):
        """Return last two digits of year."""
        return self.doomsdate.year % 100

    def first_quotient_floor(self):
        """Return quotient floor for (year / 12) (first term for doomsday summing)."""
        return self.short_year() // 12

    def first_quotient_remainder(self):
        """Return first quotient remainder (second term for doomsday summing)."""
        return self.short_year() - (self.first_quotient_floor() * 12)

    def second_quotient_floor(self):
        """Return quotient floor for (remainder / 4) (third term for doomsday summing)."""
        return self.first_quotient_remainder() // 4

    def century_anchor(self):
        """Return the century anchor (fourth term for doomsday summing)."""
        year = self.doomsdate.year
        return DoomsWeekday((year // 100 % 4) * 5 % 7 + 2)

    def year_doomsday(self):
        """Return doomsday (as a DoomsWeekday) for this year."""
        doomsday = (
            self.first_quotient_floor()
            + self.first_quotient_remainder()
            + self.second_quotient_floor()
            + self.century_anchor().number
        ) % 7
        return DoomsWeekday(doomsday)

    def year_doomsday_string(self):
        """Return a string representation of (the solution for) this year's doomsday."""
        year = self.doomsdate.year
        fqf = self.first_quotient_floor()
        fqr = self.first_quotient_remainder()
        sqf = self.second_quotient_floor()
        ca = self.century_anchor().number
        dd = self.year_doomsday()
        return (
            f"Doomsday for {year} is ({fqf} + {fqr} + {sqf} + {ca}) % 7 = "
            f"{dd.number} ({dd.name()})"
        )


class DoomsDate:
    """A custom date implementation."""

    def __init__(self, year: int, month: int, day: int) -> None:
        """Initialize object."""
        self.year = year
        self.month = month
        self.day = day

    @classmethod
    def random(cls, start, end):
        """Return a random DoomsDate between start and end (inclusive)."""
        dt_start = datetime(start.year, start.month, start.day)
        dt_end = datetime(end.year, end.month, end.day)
        dt_random = dt_start + (dt_end - dt_start) * random.random()
        return DoomsDate(dt_random.year, dt_random.month, dt_random.day)

    def doomsweekday(self):
        """Return a DoomsWeekday object for this DoomsDate."""
        return DoomsWeekday(datetime(self.year, self.month, self.day).isoweekday())

    def __str__(self) -> str:
        """Return string representation (YYYY-mm-dd)."""
        return f"{self.year}-{self.month:02}-{self.day:02}"


class DoomsWeekday:
    """A custom weekday implementation."""

    DAYS = (
        "Sunday",
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
    )

    def __init__(self, isoweekday):
        """Init method."""
        self.number = isoweekday % 7

    def __eq__(self, other) -> bool:
        """Test for object equality."""
        if isinstance(other, DoomsWeekday):
            return self.number == other.number

        return False

    def name(self):
        """Get weekday name for this DoomsWeekday."""
        return self.DAYS[self.number]

    @classmethod
    def create_from_name(cls, name):
        """Return a new DoomsWeekday from a weekday name."""
        if name in cls.DAYS:
            return DoomsWeekday(cls.DAYS.index(name))

        return None

    @classmethod
    def names_iso_order(cls):
        """Return tuple of weekday names in ISO order."""
        weekdays = list(cls.DAYS[1:])
        weekdays.append(cls.DAYS[0])
        return tuple(weekdays)
