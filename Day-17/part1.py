"""
--- Day 17: Trick Shot ---
You finally decode the Elves' message. HI, the message says. You continue searching for the sleigh keys.

Ahead of you is what appears to be a large ocean trench. Could the keys have fallen into it? You'd better send a probe to investigate.

The probe launcher on your submarine can fire the probe with any integer velocity in the x (forward) and y (upward, or downward if negative) directions. For example, an initial x,y velocity like 0,10 would fire the probe straight up, while an initial velocity like 10,-1 would fire the probe forward at a slight downward angle.

The probe's x,y position starts at 0,0. Then, it will follow some trajectory by moving in steps. On each step, these changes occur in the following order:

The probe's x position increases by its x velocity.
The probe's y position increases by its y velocity.
Due to drag, the probe's x velocity changes by 1 toward the value 0; that is, it decreases by 1 if it is greater than 0, increases by 1 if it is less than 0, or does not change if it is already 0.
Due to gravity, the probe's y velocity decreases by 1.
For the probe to successfully make it into the trench, the probe must be on some trajectory that causes it to be within a target area after any step. The submarine computer has already calculated this target area (your puzzle input). For example:

target area: x=20..30, y=-10..-5
This target area means that you need to find initial x,y velocity values such that after any step, the probe's x position is at least 20 and at most 30, and the probe's y position is at least -10 and at most -5.

Given this target area, one initial velocity that causes the probe to be within the target area after any step is 7,2:

.............#....#............
.......#..............#........
...............................
S........................#.....
...............................
...............................
...........................#...
...............................
....................TTTTTTTTTTT
....................TTTTTTTTTTT
....................TTTTTTTT#TT
....................TTTTTTTTTTT
....................TTTTTTTTTTT
....................TTTTTTTTTTT

In this diagram, S is the probe's initial position, 0,0. The x coordinate increases to the right, and the y coordinate increases upward. In the bottom right, positions that are within the target area are shown as T. After each step (until the target area is reached), the position of the probe is marked with #. (The bottom-right # is both a position the probe reaches and a position in the target area.)

Another initial velocity that causes the probe to be within the target area after any step is 6,3:

...............#..#............
...........#........#..........
...............................
......#..............#.........
...............................
...............................
S....................#.........
...............................
...............................
...............................
.....................#.........
....................TTTTTTTTTTT
....................TTTTTTTTTTT
....................TTTTTTTTTTT
....................TTTTTTTTTTT
....................T#TTTTTTTTT
....................TTTTTTTTTTT

Another one is 9,0:

S........#.....................
.................#.............
...............................
........................#......
...............................
....................TTTTTTTTTTT
....................TTTTTTTTTT#
....................TTTTTTTTTTT
....................TTTTTTTTTTT
....................TTTTTTTTTTT
....................TTTTTTTTTTT
One initial velocity that doesn't cause the probe to be within the target area after any step is 17,-4:

S..............................................................
...............................................................
...............................................................
...............................................................
.................#.............................................
....................TTTTTTTTTTT................................
....................TTTTTTTTTTT................................
....................TTTTTTTTTTT................................
....................TTTTTTTTTTT................................
....................TTTTTTTTTTT..#.............................
....................TTTTTTTTTTT................................
...............................................................
...............................................................
...............................................................
...............................................................
................................................#..............
...............................................................
...............................................................
...............................................................
...............................................................
...............................................................
...............................................................
..............................................................#
The probe appears to pass through the target area, but is never within it after any step. Instead, it continues down and to the right - only the first few steps are shown.

If you're going to fire a highly scientific probe out of a super cool probe launcher, you might as well do it with style. How high can you make the probe go while still reaching the target area?

In the above example, using an initial velocity of 6,9 is the best you can do, causing the probe to reach a maximum y position of 45. (Any higher initial y velocity causes the probe to overshoot the target area entirely.)

Find the initial velocity that causes the probe to reach the highest y position and still eventually be within the target area after any step. What is the highest y position it reaches on this trajectory?
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

    def is_within(self, point: Point) -> bool:
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
        Check if the given position is missed by the target area

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
        self.__target_area = target_area

    def __x_velocity_change(self, x_velocity: int) -> int:
        """Return -1 if x_velocity is greater than 0, 1 if x_velocity is less than 0, 0 otherwise"""
        dx = -1 if x_velocity > 0 else 1
        return dx if x_velocity != 0 else 0

    def __y_velocity_change(self, y_velocity: int) -> int:
        """Return -1 due to gravity"""
        return -1

    def launch(self, initial_pos: Point, xv_i: int, yv_i: int) -> Optional[int]:
        """
        Launch the probe with the given initial velocity

        Args:
            initial_pos (Point): The initial position of the probe
            xv_i (int): The initial x velocity
            yv_i (int): The initial y velocity

        Returns:
            Optional[int]: The maximum y position reached by the probe or
                None if the probe never reaches the target area
        """
        position = Point(initial_pos.x, initial_pos.y)
        x_velocity, y_velocity = xv_i, yv_i
        max_y = float("-inf")
        while True:
            position += Point(x_velocity, y_velocity)
            max_y = max(max_y, position.y)
            if self.__target_area.is_within(position):
                return int(max_y)
            if self.__target_area.missed_by(initial_pos, position):
                return None
            x_velocity += self.__x_velocity_change(x_velocity)
            y_velocity += self.__y_velocity_change(y_velocity)

    def best_trajectory(self, initial_pos: Point = Point(0, 0)) -> tuple[Point, int]:
        """
        Find the initial velocity that causes the probe to reach the highest y position
        and still eventually be within the target area after any step.

        Args:
            initial_pos (Point): The initial position of the probe.

        Returns:
            tuple[Point, int]: The initial velocity and the maximum y position reached by the probe.
        """
        max_y = float("-inf")
        best_initial_velocity = None
        # set range for brute force based on assumptions from data
        start_x_velocity, end_x_velocity = initial_pos.x, self.__target_area.x_max
        start_y_velocity = -max(
            abs(self.__target_area.y_min), abs(self.__target_area.y_max)
        )
        end_y_velocity = -start_y_velocity
        # brute force finding the best initial velocity
        for xv_i in range(start_x_velocity, end_x_velocity + 1):
            for yv_i in range(start_y_velocity, end_y_velocity + 1):
                y_pos = self.launch(initial_pos, xv_i, yv_i)
                if y_pos and y_pos > max_y:
                    max_y = y_pos
                    best_initial_velocity = Point(xv_i, yv_i)
        return best_initial_velocity, max_y


def main():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
        data = f.read()

    x_min, x_max, y_min, y_max = map(int, re.findall(r"(-?\d+)", data))

    target_area = TargetArea(x_min, x_max, y_min, y_max)

    launcher = ProbeLauncher(target_area)

    best_initial_velocity, max_y = launcher.best_trajectory()

    print(f"Best initial velocity: {best_initial_velocity}")
    print(f"Max y position: {max_y}")


if __name__ == "__main__":
    main()
