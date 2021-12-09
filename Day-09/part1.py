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


def is_low_point(grid, row, col):
    """
    Return whether all adjacent cells (up, down, left, right) are more than the current row, col
    """
    above = grid[row - 1][col] if row > 0 else float("inf")
    below = grid[row + 1][col] if row < len(grid) - 1 else float("inf")
    left = grid[row][col - 1] if col > 0 else float("inf")
    right = grid[row][col + 1] if col < len(grid[row]) - 1 else float("inf")
    return grid[row][col] < min(above, below, left, right)


def find_low_points(heightmap):
    low_points = []
    for row in range(len(heightmap)):
        for col in range(len(heightmap[row])):
            if is_low_point(heightmap, row, col):
                low_points.append((row, col, heightmap[row][col]))
    return low_points


def main():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
        data = f.read()

    grid = data.split("\n")
    grid = [list(map(int, row)) for row in grid]

    low_points = find_low_points(grid)

    print(f"Sum of risk levels: {sum([point[2] + 1 for point in low_points])}")


if __name__ == "__main__":
    main()
