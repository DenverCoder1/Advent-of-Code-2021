"""
--- Day 15: Chiton ---
You've almost reached the exit of the cave, but the walls are getting closer together. Your submarine can barely still fit, though; the main problem is that the walls of the cave are covered in chitons, and it would be best not to bump any of them.

The cavern is large, but has a very low ceiling, restricting your motion to two dimensions. The shape of the cavern resembles a square; a quick scan of chiton density produces a map of risk level throughout the cave (your puzzle input). For example:

1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581

You start in the top left position, your destination is the bottom right position, and you cannot move diagonally. The number at each position is its risk level; to determine the total risk of an entire path, add up the risk levels of each position you enter (that is, don't count the risk level of your starting position unless you enter it; leaving it adds no risk to your total).

Your goal is to find a path with the lowest total risk. In this example, a path with the lowest total risk is highlighted here:

[1] 1  6  3  7  5  1  7  4  2
[1] 3  8  1  3  7  3  6  7  2
[2][1][3][6][5][1][1] 3  2  8
 3  6  9  4  9  3 [1][5] 6  9
 7  4  6  3  4  1  7 [1] 1  1
 1  3  1  9  1  2  8 [1][3] 7
 1  3  5  9  9  1  2  4 [2] 1
 3  1  2  5  4  2  1  6 [3] 9
 1  2  9  3  1  3  8  5 [2][1]
 2  3  1  1  9  4  4  5  8 [1]

The total risk of this path is 40 (the starting position is never entered, so its risk is not counted).

What is the lowest total risk of any path from the top left to the bottom right?
"""

import os
from dataclasses import dataclass


@dataclass
class Tile:
    """
    Class to represent a tile in the risk map of the cave
    """

    row: int
    col: int
    risk: int


class RiskMap:
    """
    Class to represent a grid of tiles in the risk map for the cave
    """

    def __init__(self, grid: list[list[Tile]]):
        """
        Construct a risk map from a matrix of tiles

        Args:
            grid (list[list[Tile]]): A 2D matrix of tiles
        """
        self._grid = grid

    @property
    def height(self):
        return len(self._grid)

    @property
    def width(self):
        return len(self._grid[0])

    def __getitem__(self, pos: tuple[int, int]) -> Tile:
        """
        Get the tile at a position (eg. risk_map[1,2])

        Args:
            pos (tuple[int, int]): The row and column of the tile

        Returns:
            Tile: The tile at the given position in the risk map
        """
        row, col = pos
        return self._grid[row][col]

    def neighbors(self, tile: Tile) -> list[Tile]:
        """
        Get the neighbors of a tile

        Args:
            tile (Tile): The tile to get the neighbors of

        Returns:
            list[Tile]: The neighbors of the given tile
        """
        neighbors = []
        row, col = tile.row, tile.col
        if row > 0:
            neighbors.append(self._grid[row - 1][col])
        if row < self.height - 1:
            neighbors.append(self._grid[row + 1][col])
        if col > 0:
            neighbors.append(self._grid[row][col - 1])
        if col < self.width - 1:
            neighbors.append(self._grid[row][col + 1])
        return neighbors

    def min_cost(self, start: Tile, end: Tile) -> int:
        """
        Find the lowest cost path from start to end using dynamic programming

        Args:
            start (Tile): The starting tile
            end (Tile): The ending tile

        Returns:
            int: The lowest cost path from start to end
        """
        # matrix for storing the lowest total risk to reach each tile
        cost = [[float("inf") for _ in range(self.width)] for _ in range(self.height)]

        # initialize the starting position to a cost of 0
        cost[start.row][start.col] = 0

        # BFS to find the lowest cost to reach each tile
        queue = [start]
        while queue:
            current = queue.pop(0)
            for neighbor in self.neighbors(current):
                # if the current best cost to reach the neighbor is greater than the
                # cost to reach the current tile plus the risk of the neighbor,
                # update the cost to reach the neighbor to the new minimum cost
                # and add the neighbor to the queue
                neighbor_cost = cost[neighbor.row][neighbor.col]
                cost_to_neighbor = cost[current.row][current.col] + neighbor.risk
                if neighbor_cost > cost_to_neighbor:
                    cost[neighbor.row][neighbor.col] = cost_to_neighbor
                    queue.append(neighbor)

        # return the minimum cost to reach the end
        return cost[end.row][end.col]

    def __repr__(self):
        """Display a grid of numbers with no spaces"""
        return "\n".join(
            [
                "".join([str(self._grid[row][col].risk) for col in range(self.width)])
                for row in range(self.height)
            ]
        )

    @classmethod
    def from_file(cls, filename: str) -> "RiskMap":
        """
        Create a grid from a file.

        Args:
            filename (str): The name of the file to read

        Returns:
            RiskMap: The risk map created from the file
        """
        with open(filename) as f:
            data = f.read().splitlines()
        grid = [
            [Tile(row, col, int(risk)) for col, risk in enumerate(row_data)]
            for row, row_data in enumerate(data)
        ]
        return cls(grid)


def main():
    risk_map = RiskMap.from_file(os.path.join(os.path.dirname(__file__), "input.txt"))

    print(risk_map.min_cost(risk_map[0, 0], risk_map[-1, -1]))


if __name__ == "__main__":
    main()
