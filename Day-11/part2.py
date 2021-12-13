"""
--- Part Two ---
It seems like the individual flashes aren't bright enough to navigate. However, you might have a better option: the flashes seem to be synchronizing!

In the example above, the first time all octopuses flash simultaneously is step 195:

After step 193:
5877777777
8877777777
7777777777
7777777777
7777777777
7777777777
7777777777
7777777777
7777777777
7777777777

After step 194:
6988888888
9988888888
8888888888
8888888888
8888888888
8888888888
8888888888
8888888888
8888888888
8888888888

After step 195:
0000000000
0000000000
0000000000
0000000000
0000000000
0000000000
0000000000
0000000000
0000000000
0000000000

If you can calculate the exact moments when the octopuses will all flash simultaneously, you should be able to navigate through the cavern. What is the first step during which all octopuses flash?
"""

import os
from dataclasses import dataclass


@dataclass
class Point:
    x: int
    y: int
    level: int

    def __repr__(self):
        return f"Point({self.x}, {self.y}, {self.level})"


class Grid:
    def __init__(self, points: list[list[Point]], max_level: int = 9):
        self._points = points
        self._max_level = max_level

    def neighbors(self, point: Point) -> list[Point]:
        """
        Returns a list of all points adjacent to the given point including diagonals.
        """
        x = point.x
        y = point.y
        neighbors = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (
                    (i, j) == (0, 0)
                    or x + j < 0
                    or y + i < 0
                    or x + j >= len(self._points[0])
                    or y + i >= len(self._points)
                ):
                    continue
                neighbors.append(self._points[y + i][x + j])
        return neighbors

    def __increment_all_levels(self):
        """
        Increments all levels by 1.
        """
        for row in self._points:
            for point in row:
                point.level += 1

    def __flash_points(self) -> int:
        """
        Flash all points that have exceded max level by incrementing all neighboring points' levels by 1.

        Returns:
            The number of points that have flashed.
        """
        flashed = 0
        for row in self._points:
            for point in row:
                if self._max_level < point.level < float("inf"):
                    point.level = float("inf")
                    for neighbor in self.neighbors(point):
                        neighbor.level += 1
                    flashed += 1
        return flashed

    def __reset_high_levels(self):
        """
        Sets all points above max level to level 0.
        """
        for row in self._points:
            for point in row:
                if point.level > self._max_level:
                    point.level = 0

    def is_all_zero(self) -> bool:
        """
        Returns True if all points are at level 0.
        """
        return all(point.level == 0 for row in self._points for point in row)

    def advance(self, steps: int = 1) -> int:
        """
        Advances the grid a given number of steps.

        During a given step:
        - All points' levels are incremented by 1.
        - All points that exceeded max level flash by incrementing all neighboring points' levels by 1.
        - Repeat step 2 until no points are flashed (a single point can only be flashed once)
        - All points that exceeded max level are set to level 0.

        Args:
            steps (int): The number of steps to advance the grid.

        Returns:
            The number of points that have flashed.
        """
        total_flashed = 0
        for _ in range(steps):
            # Increment all levels by 1
            self.__increment_all_levels()
            # Flash all points that have exceeded max level until no points are flashed
            while flash_count := self.__flash_points():
                total_flashed += flash_count
            # Reset all points that have exceeded max level
            self.__reset_high_levels()
        return total_flashed

    def advance_until_simultaneous_flash(self) -> int:
        """
        Advances the grid until all points flash simultaneously.

        Returns:
            The number of steps taken to flash all points simultaneously.
        """
        steps = 0
        while not self.is_all_zero() or steps == 0:
            steps += 1
            self.advance()
        return steps

    def __repr__(self):
        """Display a grid of numbers where each cell is padded to a width of 3"""
        return "\n".join(
            [
                "".join(
                    [
                        (str(self._points[row][col].level)).rjust(3)
                        for col in range(len(self._points[row]))
                    ]
                )
                for row in range(len(self._points))
            ]
        )

    @classmethod
    def from_file(cls, filename: str, *, max_level: int = 9) -> "Grid":
        """
        Read a grid from a file where each line is a row of the grid and each character is the level of the point.

        Args:
            filename (str): The name of the file to read.
            max_level (int): The maximum level of a point.

        Returns:
            A Grid object.
        """
        with open(filename, "r") as f:
            lines = f.read().splitlines()
        points = [
            [Point(col, row, int(level)) for col, level in enumerate(line)]
            for row, line in enumerate(lines)
        ]
        return cls(points, max_level)


def main():
    filename = os.path.join(os.path.dirname(__file__), "input.txt")

    grid = Grid.from_file(filename, max_level=9)

    steps = grid.advance_until_simultaneous_flash()

    print(f"After {steps} steps, all points flash simultaneously.")


if __name__ == "__main__":
    main()
