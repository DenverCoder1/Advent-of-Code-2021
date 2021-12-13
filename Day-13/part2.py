"""
--- Part Two ---
Finish folding the transparent paper according to the instructions. The manual says the code is always eight capital letters.

What code do you use to activate the infrared thermal imaging camera system?
"""

import os
from dataclasses import dataclass


@dataclass
class Point:
    x: int
    y: int

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

    def __hash__(self):
        return hash((self.x, self.y))


class Paper:
    def __init__(self, dots: set[Point]):
        self.__dots = dots

    @property
    def dots(self):
        return self.__dots

    def _fold_x(self, value: int):
        """
        Fold the paper left along the x-axis, mirroring the y values across the x value for each dot

        Args:
            value: The x value to fold along.
        """
        self.__dots = {
            Point(2 * value - p.x, p.y) if p.x > value else p for p in self.__dots
        }

    def _fold_y(self, value: int):
        """
        Fold the paper up along the y-axis, mirroring the x values across the y value for each dot

        Args:
            value: The y value to fold along.
        """
        self.__dots = {
            Point(p.x, 2 * value - p.y) if p.y > value else p for p in self.__dots
        }

    def fold(self, axis: str, value: int):
        """
        Fold the paper in the given direction, mirroring across the given value

        Args:
            axis: The axis to fold along.
            value: The value to fold along.

        Raises:
            ValueError: If the axis is not x or y.
        """
        if axis == "x":
            self._fold_x(value)
        elif axis == "y":
            self._fold_y(value)
        else:
            raise ValueError(f"Invalid direction: {axis}")

    def __repr__(self):
        """Display a grid height x width of dots where empty is . and filled is #"""
        output = ""
        min_x = min(d.x for d in self.dots)
        min_y = min(d.y for d in self.dots)
        max_x = max(d.x for d in self.dots)
        max_y = max(d.y for d in self.dots)
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                if Point(x, y) in self.dots:
                    output += "#"
                else:
                    output += "."
            output += "\n"
        return output


def main():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
        dot_data, instruction_data = f.read().split("\n\n")

    dots = {
        Point(int(x), int(y))
        for x, y in (line.split(",") for line in dot_data.split("\n"))
    }

    paper = Paper(dots)

    for instruction in instruction_data.split("\n"):
        instruction = instruction.split("fold along ")[1]
        axis, value = instruction.split("=")
        value = int(value)
        paper.fold(axis, value)

    print(paper)


if __name__ == "__main__":
    main()
