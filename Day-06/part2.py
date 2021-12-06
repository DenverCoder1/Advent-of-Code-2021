"""
--- Part Two ---
Suppose the lanternfish live forever and have unlimited food and space. Would they take over the entire ocean?

After 256 days in the example above, there would be a total of 26984457539 lanternfish!

How many lanternfish would there be after 256 days?
"""

import os
from collections import defaultdict


def count_fish(initial_timers: list[int], num_days: int) -> int:
    """
    Count the number of fish after num_days.

    Args:
        initial_timers (list[int]) - the initial number of days remaining for the fish
        num_days (int) - the number of days to simulate

    Returns:
        int - the number of fish after num_days
    """
    # count how many fish there are for each number of days remaining
    day_counts = defaultdict(int)
    for timer in initial_timers:
        day_counts[timer] += 1

    # find the number of fish that will be created after num_days
    for _ in range(num_days):
        next_day_counts = defaultdict(int)
        for days_remaining, count in day_counts.items():
            # if the fish is on its last day, it will create a new fish with 8 days remaining and reset its timer to 6
            if days_remaining == 0:
                next_day_counts[6] += count
                next_day_counts[8] += count
            # otherwise, it will become a fish with one less day remaining
            else:
                next_day_counts[days_remaining - 1] += count
        # update the day_counts to be the next day's counts
        day_counts = next_day_counts

    # return the total number of fish after num_days
    return sum(day_counts.values())


def main():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
        data = f.read()

    initial_timers = [int(x) for x in data.split(",")]

    print(count_fish(initial_timers, 256))


if __name__ == "__main__":
    main()
