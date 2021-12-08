"""
--- Part Two ---
Unfortunately, considering only horizontal and vertical lines doesn't give you the full picture; you need to also consider diagonal lines.

Because of the limits of the hydrothermal vent mapping system, the lines in your list will only ever be horizontal, vertical, or a diagonal line at exactly 45 degrees. In other words:

An entry like 1,1 -> 3,3 covers points 1,1, 2,2, and 3,3.
An entry like 9,7 -> 7,9 covers points 9,7, 8,8, and 7,9.

Considering all lines from the above example would now produce the following diagram:

1.1....11.
.111...2..
..2.1.111.
...1.2.2..
.112313211
...1.2....
..1...1...
.1.....1..
1.......1.
222111....

You still need to determine the number of points where at least two lines overlap. In the above example, this is still anywhere in the diagram with a 2 or larger - now a total of 12 points.

Consider all of the lines. At how many points do at least two lines overlap?
"""


from collections import defaultdict
from typing import Optional


class Point:
    """
    Point class for representing an x,y coordinate in a grid
    """

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other: "Point"):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f"Point({self.x}, {self.y})"


class Line:
    """
    Line class for representing a pair of points in a grid
    """

    def __init__(self, start: Point, end: Point):
        self.start = start
        self.end = end

    def __eq__(self, other: "Line"):
        return self.start == other.start and self.end == other.end

    def __hash__(self):
        return hash((self.start, self.end))

    def __repr__(self):
        return f"Line({self.start}, {self.end})"

    @classmethod
    def from_string(cls, line: str) -> "Line":
        """
        Create a line from a string

        Args:
            line (str): Line in the format "x1,y1 -> x2,y2"
        """
        p1, p2 = line.split(" -> ")
        x1, y1 = p1.split(",")
        x2, y2 = p2.split(",")
        return cls(Point(int(x1), int(y1)), Point(int(x2), int(y2)))


class Grid:
    """
    Grid class for representing a grid of points stored as a dictionary for counting overlaps
    """

    def __init__(self, points: Optional[defaultdict[Point, int]] = None):
        self.points: defaultdict[Point, int] = points if points else defaultdict(int)

    def add_point(self, point: Point):
        """
        Increment the count of a point in the grid

        Args:
            point (Point): Point to add
        """
        self.points[point] += 1

    def add_line(self, line: Line):
        """
        Add a line to the grid

        Args:
            line (Line): Line to add
        """

        def compare(num1: int, num2: int) -> int:
            """Returns 0 if equal, -1 if num1 < num2, 1 if num1 > num2"""
            if num1 == num2:
                return 0
            return -1 if num1 < num2 else 1

        # determine how much x and y are changing for each step
        x_dir = compare(line.end.x, line.start.x)
        y_dir = compare(line.end.y, line.start.y)

        # add the points in the line
        x, y = line.start.x, line.start.y
        while not (x, y) == (line.end.x, line.end.y):
            self.add_point(Point(x, y))
            x, y = x + x_dir, y + y_dir
        self.add_point(Point(x, y))

    def count_overlapping_points(self) -> int:
        """
        Count the number of overlapping points

        Returns:
            int: Number of overlapping points
        """
        return sum(count >= 2 for count in self.points.values())

    def __repr__(self):
        return f"Grid({self.points})"


def main():
    # Read input
    with open("input.txt", "r") as f:
        lines = [Line.from_string(line) for line in f.readlines()]

    # Create grid
    grid = Grid()

    # Add lines
    for line in lines:
        grid.add_line(line)

    # Count overlapping points
    print(grid.count_overlapping_points())


if __name__ == "__main__":
    main()
