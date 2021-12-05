"""
-- Day 5: Hydrothermal Venture ---
You come across a field of hydrothermal vents on the ocean floor! These vents constantly produce large, opaque clouds, so it would be best to avoid them if possible.

They tend to form in lines; the submarine helpfully produces a list of nearby lines of vents (your puzzle input) for you to review. For example:

0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2

Each line of vents is given as a line segment in the format x1,y1 -> x2,y2 where x1,y1 are the coordinates of one end the line segment and x2,y2 are the coordinates of the other end. These line segments include the points at both ends. In other words:

An entry like 1,1 -> 1,3 covers points 1,1, 1,2, and 1,3.
An entry like 9,7 -> 7,7 covers points 9,7, 8,7, and 7,7.

For now, only consider horizontal and vertical lines: lines where either x1 = x2 or y1 = y2.

So, the horizontal and vertical lines from the above list would produce the following diagram:

.......1..
..1....1..
..1....1..
.......1..
.112111211
..........
..........
..........
..........
222111....

In this diagram, the top left corner is 0,0 and the bottom right corner is 9,9. Each position is shown as the number of lines which cover that point or . if no line covers that point. The top-left pair of 1s, for example, comes from 2,2 -> 2,1; the very bottom row is formed by the overlapping lines 0,9 -> 5,9 and 0,9 -> 2,9.

To avoid the most dangerous areas, you need to determine the number of points where at least two lines overlap. In the above example, this is anywhere in the diagram with a 2 or larger - a total of 5 points.

Consider only horizontal and vertical lines. At how many points do at least two lines overlap?
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
        # Horizontal line
        if line.start.y == line.end.y:
            left, right = min(line.start.x, line.end.x), max(line.start.x, line.end.x)
            for x in range(left, right + 1):
                self.add_point(Point(x, line.start.y))
        # Vertical line
        elif line.start.x == line.end.x:
            top, bottom = min(line.start.y, line.end.y), max(line.start.y, line.end.y)
            for y in range(top, bottom + 1):
                self.add_point(Point(line.start.x, y))
        # Diagonal line
        else:
            raise ValueError("Only horizontal and vertical lines are supported")

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
        try:
            grid.add_line(line)
        except ValueError:
            # Ignore lines that are not horizontal or vertical
            pass

    # Count overlapping points
    print(grid.count_overlapping_points())


if __name__ == "__main__":
    main()
