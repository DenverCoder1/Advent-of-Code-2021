"""
--- Part Two ---
Maybe a fancy trick shot isn't the best idea; after all, you only have one probe, so you had better not miss.

To get the best idea of what your options are for launching the probe, you need to find every initial velocity that causes the probe to eventually be within the target area after any step.

In the above example, there are 112 different initial velocity values that meet these criteria:

23,-10  25,-9   27,-5   29,-6   22,-6   21,-7   9,0     27,-7   24,-5
25,-7   26,-6   25,-5   6,8     11,-2   20,-5   29,-10  6,3     28,-7
8,0     30,-6   29,-8   20,-10  6,7     6,4     6,1     14,-4   21,-6
26,-10  7,-1    7,7     8,-1    21,-9   6,2     20,-7   30,-10  14,-3
20,-8   13,-2   7,3     28,-8   29,-9   15,-3   22,-5   26,-8   25,-8
25,-6   15,-4   9,-2    15,-2   12,-2   28,-9   12,-3   24,-6   23,-7
25,-10  7,8     11,-3   26,-7   7,1     23,-9   6,0     22,-10  27,-6
8,1     22,-8   13,-4   7,6     28,-6   11,-4   12,-4   26,-9   7,4
24,-10  23,-8   30,-8   7,0     9,-1    10,-1   26,-5   22,-9   6,5
7,5     23,-6   28,-10  10,-2   11,-1   20,-9   14,-2   29,-7   13,-3
23,-5   24,-8   27,-9   30,-7   28,-5   21,-10  7,9     6,6     21,-5
27,-10  7,2     30,-9   21,-8   22,-7   24,-9   20,-6   6,9     29,-5
8,-2    27,-8   30,-5   24,-7

How many distinct initial velocity values cause the probe to be within the target area after any step?
"""

import os
import re
from dataclasses import dataclass
from typing import Optional


@dataclass
class Point:
    """Class to represent a point in 2D space"""

    x: int
    y: int

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)


@dataclass
class TargetArea:
    """Class to represent the target area rectangle"""

    x_min: int
    x_max: int
    y_min: int
    y_max: int

    def contains(self, point: Point) -> bool:
        """
        Check if the given point is within the target area

        Args:
            point (Point): The point to check

        Returns:
            bool: True if the position is within the target area, False otherwise
        """
        return (
            self.x_min <= point.x <= self.x_max and self.y_min <= point.y <= self.y_max
        )

    def missed_by(self, initial_pos: Point, point: Point) -> bool:
        """
        Check if the target area is missed by the given point

        Args:
            initial_pos (Point): The position of the probe at the start
            point (Point): The current position to check

        Returns:
            bool: True if the position is missed by the target area, False otherwise
        """
        return (
            point.y < self.y_min
            or (self.x_min >= initial_pos.x and point.x > self.x_max)
            or (self.x_max <= initial_pos.x and point.x < self.x_min)
        )


class ProbeLauncher:
    """Class for simulating the launching of probes toward a target area"""

    def __init__(self, target_area: TargetArea):
        self.target_area = target_area

    def __x_velocity_change(self, x_velocity: int) -> int:
        """Return -1 if x_velocity is greater than 0, 1 if x_velocity is less than 0, 0 otherwise"""
        dx = -1 if x_velocity > 0 else 1
        return dx if x_velocity != 0 else 0

    def __y_velocity_change(self, y_velocity: int) -> int:
        """Return -1 due to gravity"""
        return -1

    def launch(self, initial_pos: Point, xv_i: int, yv_i: int) -> bool:
        """
        Launch the probe with the given initial velocity

        Args:
            initial_pos (Point): The initial position of the probe
            xv_i (int): The initial x velocity
            yv_i (int): The initial y velocity

        Returns:
            bool: True if the probe is within the target area, False otherwise
        """
        position = Point(initial_pos.x, initial_pos.y)
        x_velocity, y_velocity = xv_i, yv_i
        max_y = position.y
        while True:
            position += Point(x_velocity, y_velocity)
            max_y = max(max_y, position.y)
            if self.target_area.contains(position):
                return True
            if self.target_area.missed_by(initial_pos, position):
                return False
            x_velocity += self.__x_velocity_change(x_velocity)
            y_velocity += self.__y_velocity_change(y_velocity)

    def count_trajectories(self, initial_pos: Point = Point(0, 0)) -> int:
        """
        Count the number of trajectories that will hit the target area

        Args:
            initial_pos (Point): The initial position of the probe

        Returns:
            int: The number of trajectories that will hit the target area
        """
        # set range for brute force based on assumptions from data
        start_x_velocity, end_x_velocity = initial_pos.x, self.target_area.x_max
        end_y_velocity = max(abs(self.target_area.y_min), abs(self.target_area.y_max))
        start_y_velocity = -end_y_velocity
        # brute force finding the number of trajectories
        return sum(
            self.launch(initial_pos, xv_i, yv_i)
            for xv_i in range(start_x_velocity, end_x_velocity + 1)
            for yv_i in range(start_y_velocity, end_y_velocity + 1)
        )


def main():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
        data = f.read()

    x_min, x_max, y_min, y_max = map(int, re.findall(r"(-?\d+)", data))

    target_area = TargetArea(x_min, x_max, y_min, y_max)

    launcher = ProbeLauncher(target_area)

    print(f"Number of successful trajectories: {launcher.count_trajectories()}")


if __name__ == "__main__":
    main()
