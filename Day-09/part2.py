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


def find_basin_region(grid, low_point, basin_region: set, from_direction: int = None):
    """
    Recursively expand region until walls are reached and return the list of points in the region

    Walls are denoted by 9's
    """
    row, col, height = low_point
    if (
        height == 9
        or row < 0
        or row >= len(grid)
        or col < 0
        or col >= len(grid[0])
        or low_point in basin_region
    ):
        return []
    basin_region.add(low_point)
    if row > 0 and grid[row - 1][col] != 9:
        left_region = find_basin_region(grid, (row - 1, col, height), basin_region, -1)
        for point in left_region:
            basin_region.add(point)
    if row < len(grid) - 1 and grid[row + 1][col] != 9:
        right_region = find_basin_region(grid, (row + 1, col, height), basin_region, 1)
        for point in right_region:
            basin_region.add(point)
    if col > 0 and grid[row][col - 1] != 9:
        up_region = find_basin_region(grid, (row, col - 1, height), basin_region, 2)
        for point in up_region:
            basin_region.add(point)
    if col < len(grid[row]) - 1 and grid[row][col + 1] != 9:
        down_region = find_basin_region(grid, (row, col + 1, height), basin_region, -2)
        for point in down_region:
            basin_region.add(point)
    return basin_region


def find_basins(grid):
    """basins are sets of points separated by a wall of 9's"""
    low_points = find_low_points(grid)
    basins = []
    for low_point in low_points:
        basins.append(find_basin_region(grid, low_point, set()))
    return basins


def main():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
        data = f.read()

    grid = data.split("\n")
    grid = [list(map(int, row)) for row in grid]

    basins = find_basins(grid)

    # extract the three largest basins
    basins.sort(key=lambda basin: len(basin), reverse=True)
    largest_basins = basins[:3]

    # multiply the sizes of the three largest basins
    product = 1
    for basin in largest_basins:
        product *= len(basin)
    print(product)


if __name__ == "__main__":
    main()
