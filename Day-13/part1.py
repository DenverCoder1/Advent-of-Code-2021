"""
--- Day 13: Transparent Origami ---
You reach another volcanically active part of the cave. It would be nice if you could do some kind of thermal imaging so you could tell ahead of time which caves are too hot to safely enter.

Fortunately, the submarine seems to be equipped with a thermal camera! When you activate it, you are greeted with:

Congratulations on your purchase! To activate this infrared thermal imaging
camera system, please enter the code found on page 1 of the manual.
Apparently, the Elves have never used this feature. To your surprise, you manage to find the manual; as you go to open it, page 1 falls out. It's a large sheet of transparent paper! The transparent paper is marked with random dots and includes instructions on how to fold it up (your puzzle input). For example:

6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5

The first section is a list of dots on the transparent paper. 0,0 represents the top-left coordinate. The first value, x, increases to the right. The second value, y, increases downward. So, the coordinate 3,0 is to the right of 0,0, and the coordinate 0,7 is below 0,0. The coordinates in this example form the following pattern, where # is a dot on the paper and . is an empty, unmarked position:

...#..#..#.
....#......
...........
#..........
...#....#.#
...........
...........
...........
...........
...........
.#....#.##.
....#......
......#...#
#..........
#.#........
Then, there is a list of fold instructions. Each instruction indicates a line on the transparent paper and wants you to fold the paper up (for horizontal y=... lines) or left (for vertical x=... lines). In this example, the first fold instruction is fold along y=7, which designates the line formed by all of the positions where y is 7 (marked here with -):

...#..#..#.
....#......
...........
#..........
...#....#.#
...........
...........
-----------
...........
...........
.#....#.##.
....#......
......#...#
#..........
#.#........
Because this is a horizontal line, fold the bottom half up. Some of the dots might end up overlapping after the fold is complete, but dots will never appear exactly on a fold line. The result of doing this fold looks like this:

#.##..#..#.
#...#......
......#...#
#...#......
.#.#..#.###
...........
...........
Now, only 17 dots are visible.

Notice, for example, the two dots in the bottom left corner before the transparent paper is folded; after the fold is complete, those dots appear in the top left corner (at 0,0 and 0,1). Because the paper is transparent, the dot just below them in the result (at 0,3) remains visible, as it can be seen through the transparent paper.

Also notice that some dots can end up overlapping; in this case, the dots merge together and become a single dot.

The second fold instruction is fold along x=5, which indicates this line:

#.##.|#..#.
#...#|.....
.....|#...#
#...#|.....
.#.#.|#.###
.....|.....
.....|.....
Because this is a vertical line, fold left:

#####
#...#
#...#
#...#
#####
.....
.....
The instructions made a square!

The transparent paper is pretty big, so for now, focus on just completing the first fold. After the first fold in the example above, 17 dots are visible - dots that end up overlapping after the fold is completed count as a single dot.

How many dots are visible after completing just the first fold instruction on your transparent paper?
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
        self.dots = dots
        self.width = max(d.x for d in dots) + 1
        self.height = max(d.y for d in dots) + 1

    def fold_x(self, value: int):
        """fold left along an x value, mirroring the y values across the x value for each dot"""
        self.dots = {
            Point(2 * value - p.x, p.y) if p.x > value else p for p in self.dots
        }

    def fold_y(self, value: int):
        """fold up along an y value, mirroring the x values across the y value for each dot"""
        self.dots = {
            Point(p.x, 2 * value - p.y) if p.y > value else p for p in self.dots
        }

    def fold(self, direction: str, value: int):
        if direction == "x":
            self.fold_x(value)
        elif direction == "y":
            self.fold_y(value)
        else:
            raise ValueError(f"Invalid direction: {direction}")

    def __repr__(self):
        """print a grid height x width of dots where empty is . and filled is #"""
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

    instruction = instruction_data.split("\n")[0].split("fold along ")[1]
    direction, value = instruction.split("=")
    value = int(value)

    paper.fold(direction, value)

    print(len(paper.dots))


if __name__ == "__main__":
    main()
