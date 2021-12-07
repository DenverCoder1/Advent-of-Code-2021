"""
--- Part Two ---
The crabs don't seem interested in your proposed solution. Perhaps you misunderstand crab engineering?

As it turns out, crab submarine engines don't burn fuel at a constant rate. Instead, each change of 1 step in horizontal position costs 1 more unit of fuel than the last: the first step costs 1, the second step costs 2, the third step costs 3, and so on.

As each crab moves, moving further becomes more expensive. This changes the best horizontal position to align them all on; in the example above, this becomes 5:

Move from 16 to 5: 66 fuel
Move from 1 to 5: 10 fuel
Move from 2 to 5: 6 fuel
Move from 0 to 5: 15 fuel
Move from 4 to 5: 1 fuel
Move from 2 to 5: 6 fuel
Move from 7 to 5: 3 fuel
Move from 1 to 5: 10 fuel
Move from 2 to 5: 6 fuel
Move from 14 to 5: 45 fuel
This costs a total of 168 fuel. This is the new cheapest possible outcome; the old alignment position (2) now costs 206 fuel instead.

Determine the horizontal position that the crabs can align to using the least fuel possible so they can make you an escape route! How much fuel must they spend to align to that position?
"""

import os


def calculate_fuel(position1: int, position2: int) -> int:
    """
    Calculate fuel usage between two positions (the distance between them)

    Args:
        position1 (int): The starting position
        position2 (int): The position to which the distance is calculated

    Returns:
        int: The fuel usage between the two positions
    """
    return abs(position1 - position2) * (abs(position1 - position2) + 1) // 2


def find_min_fuel(positions: list[int]) -> tuple[int, int]:
    """
    Find the number to which the sum of fuel usage from all other positions is minimized

    Args:
        positions (list[int]): The list of positions

    Returns:
        int: The position to which the sum of fuel usage from all other positions is minimized
        int: The minimum fuel required to align the positions
    """
    min_fuel = min_fuel_position = float("inf")
    for target in range(len(positions)):
        fuel = sum(calculate_fuel(target, position) for position in positions)
        if fuel < min_fuel:
            min_fuel, min_fuel_position = fuel, target
    return min_fuel_position, min_fuel


def main():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
        data = [int(x) for x in f.read().split(",")]

    min_fuel_position, min_fuel = find_min_fuel(data)

    print(f"The position to which the minimum fuel is required is {min_fuel_position}.")
    print(f"The minimum fuel required to align the positions is {min_fuel}.")


if __name__ == "__main__":
    main()
