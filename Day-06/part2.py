"""
--- Part Two ---
Suppose the lanternfish live forever and have unlimited food and space. Would they take over the entire ocean?

After 256 days in the example above, there would be a total of 26984457539 lanternfish!

How many lanternfish would there be after 256 days?
"""

import os
from typing import Optional


class FishCalendar:
    """
    A class to model a calendar of fish reproduction cycles.

    Attributes:
        day_counts (list[int]) : A list where each element is the number of fish for each
            number of days remaining, where the index of the list is the number of days remaining
            (i.e. day_counts[0] is the number of fish with 0 days remaining).
        cycle_length (int) : The length of the fish cycle.
        first_cycle_length (int) : The length of a fish's first cycle.
        fish_count (int) : The number of fish in the calendar.
    """

    def __init__(
        self,
        cycle_length: int,
        first_cycle_length: int,
        day_counts: Optional[list[int]] = None,
    ):
        """
        Initialize a FishCalendar object.

        Args:
            cycle_length (int) : The length of the fish cycle.
            first_cycle_length (int) : The length of a fish's first cycle.
            day_counts (Optional[list[int]]) : A list where each element is the number of fish for each
                number of days remaining, where the index of the list is the number of days remaining
                (i.e. day_counts[0] is the number of fish with 0 days remaining).
        """
        self.__cycle_length = cycle_length
        self.__first_cycle_length = first_cycle_length
        self.__day_counts = (
            day_counts.copy()
            if day_counts is not None
            else [0] * max(cycle_length, first_cycle_length)
        )

    @property
    def day_counts(self) -> list[int]:
        return self.__day_counts

    @property
    def cycle_length(self) -> int:
        return self.__cycle_length

    @property
    def first_cycle_length(self) -> int:
        return self.__first_cycle_length

    @property
    def fish_count(self):
        """Return the total number of fish in the calendar."""
        return sum(self.day_counts)

    def get_count_at_day(self, day: int) -> int:
        """
        Get the number of fish with the given number of days remaining.

        Args:
            day (int) : The number of days remaining.

        Returns:
            int : The number of fish with the given number of days remaining.
        """
        return self.__day_counts[day]

    def shift_day_counts(self):
        """
        Shift all of the day counts to the left by one day.
        """
        self.__day_counts = self.__day_counts[1:] + [0]

    def add_fish(self, day: int, amount: int = 1):
        """
        Add a given number of fish with the given number of days remaining.

        Args:
            day (int) : The number of days remaining.
            amount (int) : The number of fish to add (default 1).
        """
        self.__day_counts[day] += amount

    def increment_calendar_day(self):
        """
        Increment the fish calendar by one day, resetting fish that have reached the end of their cycle,
        adding new fish, and decreasing the number of days remaining for each fish that is not at the end of its cycle.
        """
        num_fish_on_day_zero = self.get_count_at_day(0)

        # Move all fish counts to the left by one day
        self.shift_day_counts()

        # Reset fish that have reached the end of their cycle
        self.add_fish(self.cycle_length - 1, amount=num_fish_on_day_zero)

        # Add a new fish for every fish that reached the end of their cycle
        self.add_fish(self.first_cycle_length - 1, amount=num_fish_on_day_zero)

    def simulate(self, num_days: int) -> int:
        """
        Simulate the fish calendar for the given number of days.

        Args:
            num_days (int) : The number of days to simulate.

        Returns:
            int : The number of fish after the given number of days.
        """
        for _ in range(num_days):
            self.increment_calendar_day()

        return self.fish_count

    def __repr__(self):
        """Return a string representation of the FishCalendar object."""
        return f"FishCalendar(day_counts={self.day_counts}, cycle_length={self.cycle_length}, first_cycle_length={self.first_cycle_length})"

    @classmethod
    def from_file(cls, file_path: str, *, cycle_length: int, first_cycle_length: int):
        """
        Initialize a FishCalendar object from a file containing days remaining for each fish.

        Args:
            file_path (str) : The path to the file containing the fish times.
            cycle_length (int) : The length of the fish cycle.
            first_cycle_length (int) : The length of a fish's first cycle.

        Returns:
            FishCalendar : A FishCalendar object.
        """
        with open(file_path, "r") as file:
            data = file.read()

        fish_calendar = cls(cycle_length, first_cycle_length)

        # Set the fish counts
        for days_remaining in data.split(","):
            fish_calendar.add_fish(int(days_remaining))

        return fish_calendar


def main():
    """
    Main function.
    """

    lanternfish_calendar = FishCalendar.from_file(
        os.path.join(os.path.dirname(__file__), "input.txt"),
        cycle_length=7,
        first_cycle_length=9,
    )

    # Find the number of fish after the 256 days
    print(lanternfish_calendar.simulate(256))


if __name__ == "__main__":
    main()
