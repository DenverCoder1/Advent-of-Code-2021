"""
--- Part Two ---
After reviewing the available paths, you realize you might have time to visit a single small cave twice. Specifically, big caves can be visited any number of times, a single small cave can be visited at most twice, and the remaining small caves can be visited at most once. However, the caves named start and end can only be visited exactly once each: once you leave the start cave, you may not return to it, and once you reach the end cave, the path must end immediately.

Now, the 36 possible paths through the first example above are:

start,A,b,A,b,A,c,A,end
start,A,b,A,b,A,end
start,A,b,A,b,end
start,A,b,A,c,A,b,A,end
start,A,b,A,c,A,b,end
start,A,b,A,c,A,c,A,end
start,A,b,A,c,A,end
start,A,b,A,end
start,A,b,d,b,A,c,A,end
start,A,b,d,b,A,end
start,A,b,d,b,end
start,A,b,end
start,A,c,A,b,A,b,A,end
start,A,c,A,b,A,b,end
start,A,c,A,b,A,c,A,end
start,A,c,A,b,A,end
start,A,c,A,b,d,b,A,end
start,A,c,A,b,d,b,end
start,A,c,A,b,end
start,A,c,A,c,A,b,A,end
start,A,c,A,c,A,b,end
start,A,c,A,c,A,end
start,A,c,A,end
start,A,end
start,b,A,b,A,c,A,end
start,b,A,b,A,end
start,b,A,b,end
start,b,A,c,A,b,A,end
start,b,A,c,A,b,end
start,b,A,c,A,c,A,end
start,b,A,c,A,end
start,b,A,end
start,b,d,b,A,c,A,end
start,b,d,b,A,end
start,b,d,b,end
start,b,end
The slightly larger example above now has 103 paths through it, and the even larger example now has 3509 paths through it.

Given these new rules, how many paths through this cave system are there?
"""

import os
from collections import defaultdict


class Graph:
    def __init__(self):
        self._nodes: defaultdict[str, list] = defaultdict(list)

    def add_edge(self, node: str, neighbor: str):
        """Add an edge to the graph going in both directions"""
        self._nodes[node].append(neighbor)
        self._nodes[neighbor].append(node)

    def get_neighbors(self, node: str) -> list[str]:
        """Get the neighbors of a given node"""
        return self._nodes[node]

    def is_small_cave(self, node: str) -> bool:
        """Check if a node is a small cave (i.e. it contains only lowercase letters)"""
        return node.islower()

    def __dfs_count(
        self,
        current: str,
        start: str,
        end: str,
        visited: set,
        can_visit_twice: bool = True,
    ) -> int:
        """
        Using DFS, recursively find all paths from start to end that visit small caves at most once,
        with the exception of a single small cave that can be visited twice.
        Large caves can be visited any number of times.

        Args:
            current (str): The current node
            start (str): The starting node
            end (str): The ending node
            visited (set): The set of visited nodes
            can_visit_twice (bool): Whether or not it is permitted to add a visited small cave a second time

        Returns:
            int: The number of paths
        """
        if current == end:
            return 1

        count = 0

        # add up paths from visiting each neighbor
        for neighbor in self.get_neighbors(current):
            # visit if node is a large cave or a small cave that has not been visited before
            if not self.is_small_cave(neighbor) or neighbor not in visited:
                count += self.__dfs_count(
                    neighbor, start, end, visited | {neighbor}, can_visit_twice
                )
            # if it's a small cave and we still can visit a small cave twice
            elif can_visit_twice and neighbor not in {start, end}:
                # add the rest of the paths while not visiting the same small cave twice
                count += self.__dfs_count(
                    neighbor, start, end, visited | {neighbor}, False
                )

        return count

    def find_path_count(self, start: str, end: str) -> int:
        """
        Count paths from start to end by calling the recursive helper function __dfs_count

        Args:
            start (str): The starting node
            end (str): The ending node

        Returns:
            int: The number of paths
        """
        return self.__dfs_count(current=start, start=start, end=end, visited={start})

    def __str__(self):
        return str(self._nodes)

    @classmethod
    def from_file(cls, filename: str) -> "Graph":
        """
        Create a graph from a file

        Args:
            filename (str): The filename

        Returns:
            Graph: The graph
        """
        graph = cls()
        with open(filename) as f:
            data = f.read().splitlines()
        for line in data:
            node, neighbor = line.split("-")
            graph.add_edge(node, neighbor)
        return graph


def main():
    filename = os.path.join(os.path.dirname(__file__), "input.txt")

    graph = Graph.from_file(filename)

    print(graph.find_path_count("start", "end"))


if __name__ == "__main__":
    main()
