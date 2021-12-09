"""
--- Part Two ---
Next, you need to find the largest basins so you know what areas are most important to avoid.

A basin is all locations that eventually flow downward to a single low point. Therefore, every low point has a basin, although some basins are very small. Locations of height 9 do not count as being in any basin, and all other locations will always be part of exactly one basin.

The size of a basin is the number of locations within the basin, including the low point. The example above has four basins.

The top-left basin, size 3:

2199943210
3987894921
9856789892
8767896789
9899965678
The top-right basin, size 9:

2199943210
3987894921
9856789892
8767896789
9899965678
The middle basin, size 14:

2199943210
3987894921
9856789892
8767896789
9899965678
The bottom-right basin, size 9:

2199943210
3987894921
9856789892
8767896789
9899965678
Find the three largest basins and multiply their sizes together. In the above example, this is 9 * 14 * 9 = 1134.

What do you get if you multiply together the sizes of the three largest basins?
"""

import os
from dataclasses import dataclass
from functools import reduce


@dataclass
class Point:
    """
    Class to represent a point in the Heightmap
    """

    row: int
    col: int
    height: int

    @property
    def risk_level(self):
        return 1 + self.height

    def __int__(self):
        return self.height

    def __lt__(self, other):
        if isinstance(other, Point):
            return self.height < other.height
        return self.height < other

    def __gt__(self, other):
        if isinstance(other, Point):
            return self.height > other.height
        return self.height > other

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.height == other.height
        return self.height == other

    def __hash__(self):
        return hash((self.row, self.col, self.height))


class Heightmap:
    """
    Class to represent a heightmap containing a grid of Points.
    """

    def __init__(self, data: list[list[int]]):
        self.points = [
            [Point(row, col, height) for col, height in enumerate(data[row])]
            for row in range(len(data))
        ]

    def __is_low_point(self, point: Point) -> bool:
        """
        Return whether all adjacent cells (up, down, left, right) are higher than the current row, col

        Args:
            heightmap (Heightmap): The heightmap containing the grid of all points
            point (Point): The point to check

        Returns:
            bool: Whether the point is a low point or not
        """
        row, col = point.row, point.col
        above = self[row - 1][col] if row > 0 else float("inf")
        below = self[row + 1][col] if row < len(self) - 1 else float("inf")
        left = self[row][col - 1] if col > 0 else float("inf")
        right = self[row][col + 1] if col < len(self[row]) - 1 else float("inf")
        return self[row][col] < min(above, below, left, right)

    def find_low_points(self) -> list[Point]:
        """
        Return a list of all low points in the heightmap

        Args:
            heightmap (Heightmap): The heightmap containing the grid of all points

        Returns:
            list[Point]: A list of all low points in the heightmap
        """
        return [point for row in self for point in row if self.__is_low_point(point)]

    def find_basin_region(self, point: Point, basin: set[Point]) -> set[Point]:
        """
        Recursively expand region until walls are reached and return the list of points in the region

        Args:
            heightmap (Heightmap): The heightmap containing the grid of all points
            point (Point): The point currently being expanded
            basin (set[Point]): The current basin region

        Returns:
            set[Point]: The basin region
        """
        row, col = point.row, point.col

        # don't expand if we've already seen this point
        if point in basin:
            return set()

        # add the current point to the basin
        basin.add(point)

        # expand region upward
        if row > 0 and self[row - 1][col] != 9:
            basin.update(self.find_basin_region(self[row - 1][col], basin))

        # expand region downward
        if row < len(self) - 1 and self[row + 1][col] != 9:
            basin.update(self.find_basin_region(self[row + 1][col], basin))

        # expand region to the left
        if col > 0 and self[row][col - 1] != 9:
            basin.update(self.find_basin_region(self[row][col - 1], basin))

        # expand region to the right
        if col < len(self[row]) - 1 and self[row][col + 1] != 9:
            basin.update(self.find_basin_region(self[row][col + 1], basin))

        # return the basin region
        return basin

    def find_basins(self) -> list[set[Point]]:
        """
        Locate all basins in the heightmap.

        Note: basins are sets of points bounded by a wall of 9's

        Args:
            heightmap (Heightmap): The heightmap containing the grid of all points

        Returns:
            list[set[Point]]: A list of all basins in the heightmap
        """
        low_points = self.find_low_points()
        return [self.find_basin_region(low_point, set()) for low_point in low_points]

    def __getitem__(self, key):
        return self.points[key]

    def __len__(self):
        return len(self.points)

    def __iter__(self):
        for row in self.points:
            yield row

    def __repr__(self):
        return "".join(
            "".join(f"{point.height}" for point in row) + "\n" for row in self.points
        )


def main():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
        data = [list(map(int, row)) for row in f.read().splitlines()]

    heightmap = Heightmap(data)

    basins = heightmap.find_basins()

    # extract the three largest basins
    largest_basins = sorted(basins, key=lambda basin: len(basin), reverse=True)[:3]

    # multiply the sizes of the three largest basins
    print(reduce(lambda x, y: x * y, [len(basin) for basin in largest_basins]))


if __name__ == "__main__":
    main()
