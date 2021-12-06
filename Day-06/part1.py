"""
-- Day 6: Lanternfish ---
The sea floor is getting steeper. Maybe the sleigh keys got carried this way?

A massive school of glowing lanternfish swims past. They must spawn quickly to reach such large numbers - maybe exponentially quickly? You should model their growth rate to be sure.

Although you know nothing about this specific species of lanternfish, you make some guesses about their attributes. Surely, each lanternfish creates a new lanternfish once every 7 days.

However, this process isn't necessarily synchronized between every lanternfish - one lanternfish might have 2 days left until it creates another lanternfish, while another might have 4. So, you can model each fish as a single number that represents the number of days until it creates a new lanternfish.

Furthermore, you reason, a new lanternfish would surely need slightly longer before it's capable of producing more lanternfish: two more days for its first cycle.

So, suppose you have a lanternfish with an internal timer value of 3:

After one day, its internal timer would become 2.
After another day, its internal timer would become 1.
After another day, its internal timer would become 0.
After another day, its internal timer would reset to 6, and it would create a new lanternfish with an internal timer of 8.
After another day, the first lanternfish would have an internal timer of 5, and the second lanternfish would have an internal timer of 7.

A lanternfish that creates a new fish resets its timer to 6, not 7 (because 0 is included as a valid timer value). The new lanternfish starts with an internal timer of 8 and does not start counting down until the next day.

Realizing what you're trying to do, the submarine automatically produces a list of the ages of several hundred nearby lanternfish (your puzzle input). For example, suppose you were given the following list:

3,4,3,1,2
This list means that the first fish has an internal timer of 3, the second fish has an internal timer of 4, and so on until the fifth fish, which has an internal timer of 2. Simulating these fish over several days would proceed as follows:

Initial state: 3,4,3,1,2
After  1 day:  2,3,2,0,1
After  2 days: 1,2,1,6,0,8
After  3 days: 0,1,0,5,6,7,8
After  4 days: 6,0,6,4,5,6,7,8,8
After  5 days: 5,6,5,3,4,5,6,7,7,8
After  6 days: 4,5,4,2,3,4,5,6,6,7
After  7 days: 3,4,3,1,2,3,4,5,5,6
After  8 days: 2,3,2,0,1,2,3,4,4,5
After  9 days: 1,2,1,6,0,1,2,3,3,4,8
After 10 days: 0,1,0,5,6,0,1,2,2,3,7,8
After 11 days: 6,0,6,4,5,6,0,1,1,2,6,7,8,8,8
After 12 days: 5,6,5,3,4,5,6,0,0,1,5,6,7,7,7,8,8
After 13 days: 4,5,4,2,3,4,5,6,6,0,4,5,6,6,6,7,7,8,8
After 14 days: 3,4,3,1,2,3,4,5,5,6,3,4,5,5,5,6,6,7,7,8
After 15 days: 2,3,2,0,1,2,3,4,4,5,2,3,4,4,4,5,5,6,6,7
After 16 days: 1,2,1,6,0,1,2,3,3,4,1,2,3,3,3,4,4,5,5,6,8
After 17 days: 0,1,0,5,6,0,1,2,2,3,0,1,2,2,2,3,3,4,4,5,7,8
After 18 days: 6,0,6,4,5,6,0,1,1,2,6,0,1,1,1,2,2,3,3,4,6,7,8,8,8,8

Each day, a 0 becomes a 6 and adds a new 8 to the end of the list, while each other number decreases by 1 if it was present at the start of the day.

In this example, after 18 days, there are a total of 26 fish. After 80 days, there would be a total of 5934.

Find a way to simulate lanternfish. How many lanternfish would there be after 80 days?
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

    def set_count_at_day(self, day: int, count: int):
        """
        Set the number of fish with the given number of days remaining.

        Args:
            day (int) : The number of days remaining.
            count (int) : The number of fish with the given number of days remaining.
        """
        self.__day_counts[day] = count

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

        # Move all fish counts down by one day
        for i in range(len(self.day_counts) - 1):
            self.set_count_at_day(i, self.get_count_at_day(i + 1))
        self.set_count_at_day(len(self.day_counts) - 1, 0)

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

    # Find the number of fish after the 80 days
    print(lanternfish_calendar.simulate(80))


if __name__ == "__main__":
    main()
