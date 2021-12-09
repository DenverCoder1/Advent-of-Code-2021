"""
-- Day 9: Smoke Basin ---
These caves seem to be lava tubes. Parts are even still volcanically active; small hydrothermal vents release smoke into the caves that slowly settles like rain.

If you can model how the smoke flows through the caves, you might be able to avoid it and be that much safer. The submarine generates a heightmap of the floor of the nearby caves for you (your puzzle input).

Smoke flows to the lowest point of the area it's in. For example, consider the following heightmap:

2199943210
3987894921
9856789892
8767896789
9899965678

Each number corresponds to the height of a particular location, where 9 is the highest and 0 is the lowest a location can be.

Your first goal is to find the low points - the locations that are lower than any of its adjacent locations. Most locations have four adjacent locations (up, down, left, and right); locations on the edge or corner of the map have three or two adjacent locations, respectively. (Diagonal locations do not count as adjacent.)

In the above example, there are four low points, all highlighted: two are in the first row (a 1 and a 0), one is in the third row (a 5), and one is in the bottom row (also a 5). All other locations on the heightmap have some lower adjacent location, and so are not low points.

The risk level of a low point is 1 plus its height. In the above example, the risk levels of the low points are 2, 1, 6, and 6. The sum of the risk levels of all low points in the heightmap is therefore 15.

Find all of the low points on your heightmap. What is the sum of the risk levels of all low points on your heightmap?


"""

import os
from dataclasses import dataclass


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
        self.points: list[Point] = [
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

    low_points = heightmap.find_low_points()

    print(f"Sum of risk levels: {sum([point.risk_level for point in low_points])}")


if __name__ == "__main__":
    main()
