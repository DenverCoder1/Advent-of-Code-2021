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
class Node:
    row: int
    col: int
    weight: int


class Grid:
    def __init__(self, data: list[list[Node]]):
        self._data = data
        self._height = len(data)
        self._width = len(data[0])

    def __getitem__(self, pos: tuple[int, int]) -> Node:
        """
        Get the node at a position (eg. grid[1,2])

        Args:
            pos (tuple): The row and column of the node

        Returns:
            Node: The node at the given position in the grid
        """
        row, col = pos
        return self._data[row][col]

    def neighbors(self, node: Node):
        """
        Get the neighbors of a position.
        """
        neighbors = []
        row, col = node.row, node.col
        if row > 0:
            neighbors.append(self._data[row - 1][col])
        if row < self._height - 1:
            neighbors.append(self._data[row + 1][col])
        if col > 0:
            neighbors.append(self._data[row][col - 1])
        if col < self._width - 1:
            neighbors.append(self._data[row][col + 1])
        return neighbors

    def min_cost(self, start: Node, end: Node) -> int:
        """
        Find the lowest cost path from start to end using dynamic programming

        Args:
            start (tuple): The x,y coordinates of the starting position
            end (tuple): The x,y coordinates of the ending position

        Returns:
            int: The lowest cost path from start to end
        """
        # matrix for storing the lowest cost to reach each node
        cost = [[float("inf") for _ in range(self._width)] for _ in range(self._height)]

        # initialize the starting position to a cost of 0
        cost[start.row][start.col] = 0

        # BFS to find the lowest cost to reach each node
        queue = [start]
        while queue:
            current = queue.pop(0)
            neighbors = self.neighbors(current)
            for neighbor in neighbors:
                # if the current best cost to reach the neighbor is greater than the
                # cost to reach the current node plus the weight of the neighbor,
                # update the cost to reach the neighbor to the new minimum cost
                # and add the neighbor to the queue
                neighbor_cost = cost[neighbor.row][neighbor.col]
                cost_to_neighbor = cost[current.row][current.col] + neighbor.weight
                if neighbor_cost > cost_to_neighbor:
                    cost[neighbor.row][neighbor.col] = cost_to_neighbor
                    queue.append(neighbor)

        # return the minimum cost to reach the end
        return cost[end.row][end.col]

    @classmethod
    def from_file(cls, filename: str) -> "Grid":
        """
        Create a grid from a file.

        Args:
            filename (str): The name of the file to read

        Returns:
            Grid: The grid created from the file
        """
        with open(filename) as f:
            data = f.read().splitlines()

        grid = [
            [Node(row, col, int(weight)) for col, weight in enumerate(row_data)]
            for row, row_data in enumerate(data)
        ]
        return cls(grid)


def main():
    grid = Grid.from_file(os.path.join(os.path.dirname(__file__), "input.txt"))

    print(grid.min_cost(grid[0, 0], grid[-1, -1]))


if __name__ == "__main__":
    main()
