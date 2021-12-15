"""
--- Part Two ---
Now that you know how to find low-risk paths in the cave, you can try to find your way out.

The entire cave is actually five times larger in both dimensions than you thought; the area you originally scanned is just one tile in a 5x5 tile area that forms the full map. Your original map tile repeats to the right and downward; each time the tile repeats to the right or downward, all of its risk levels are 1 higher than the tile immediately up or left of it. However, risk levels above 9 wrap back around to 1. So, if your original map had some position with a risk level of 8, then that same position on each of the 25 total tiles would be as follows:

8 9 1 2 3
9 1 2 3 4
1 2 3 4 5
2 3 4 5 6
3 4 5 6 7

Each single digit above corresponds to the example position with a value of 8 on the top-left tile. Because the full map is actually five times larger in both dimensions, that position appears a total of 25 times, once in each duplicated tile, with the values shown above.

Here is the full five-times-as-large version of the first example above, with the original map in the top left corner highlighted:

1163751742|2274862853|3385973964|4496184175|5517295286
1381373672|2492484783|3513595894|4624616915|5735727126
2136511328|3247622439|4358733541|5469844652|6571955763
3694931569|4715142671|5826253782|6937364893|7148475914
7463417111|8574528222|9685639333|1796741444|2817852555
1319128137|2421239248|3532341359|4643452461|5754563572
1359912421|2461123532|3572234643|4683345754|5794456865
3125421639|4236532741|5347643852|6458754963|7569865174
1293138521|2314249632|3425351743|4536462854|5647573965
2311944581|3422155692|4533266713|5644377824|6755488935
----------+----------+----------+----------+----------
2274862853|3385973964|4496184175|5517295286|6628316397
2492484783|3513595894|4624616915|5735727126|6846838237
3247622439|4358733541|5469844652|6571955763|7682166874
4715142671|5826253782|6937364893|7148475914|8259586125
8574528222|9685639333|1796741444|2817852555|3928963666
2421239248|3532341359|4643452461|5754563572|6865674683
2461123532|3572234643|4683345754|5794456865|6815567976
4236532741|5347643852|6458754963|7569865174|8671976285
2314249632|3425351743|4536462854|5647573965|6758684176
3422155692|4533266713|5644377824|6755488935|7866599146
----------+----------+----------+----------+----------
3385973964|4496184175|5517295286|6628316397|7739427418
3513595894|4624616915|5735727126|6846838237|7957949348
4358733541|5469844652|6571955763|7682166874|8793277985
5826253782|6937364893|7148475914|8259586125|9361697236
9685639333|1796741444|2817852555|3928963666|4139174777
3532341359|4643452461|5754563572|6865674683|7976785794
3572234643|4683345754|5794456865|6815567976|7926678187
5347643852|6458754963|7569865174|8671976285|9782187396
3425351743|4536462854|5647573965|6758684176|7869795287
4533266713|5644377824|6755488935|7866599146|8977611257
----------+----------+----------+----------+----------
4496184175|5517295286|6628316397|7739427418|8841538529
4624616915|5735727126|6846838237|7957949348|8168151459
5469844652|6571955763|7682166874|8793277985|9814388196
6937364893|7148475914|8259586125|9361697236|1472718347
1796741444|2817852555|3928963666|4139174777|5241285888
4643452461|5754563572|6865674683|7976785794|8187896815
4683345754|5794456865|6815567976|7926678187|8137789298
6458754963|7569865174|8671976285|9782187396|1893298417
4536462854|5647573965|6758684176|7869795287|8971816398
5644377824|6755488935|7866599146|8977611257|9188722368
----------+----------+----------+----------+----------
5517295286|6628316397|7739427418|8841538529|9952649631
5735727126|6846838237|7957949348|8168151459|9279262561
6571955763|7682166874|8793277985|9814388196|1925499217
7148475914|8259586125|9361697236|1472718347|2583829458
2817852555|3928963666|4139174777|5241285888|6352396999
5754563572|6865674683|7976785794|8187896815|9298917926
5794456865|6815567976|7926678187|8137789298|9248891319
7569865174|8671976285|9782187396|1893298417|2914319528
5647573965|6758684176|7869795287|8971816398|9182927419
6755488935|7866599146|8977611257|9188722368|1299833479

Equipped with the full map, you can now find a path from the top left corner to the bottom right corner with the lowest total risk:

[1]1637517422274862853338597396444961841755517295286
[1]3813736722492484783351359589446246169155735727126
[2]1365113283247622439435873354154698446526571955763
[3]6949315694715142671582625378269373648937148475914
[7]4634171118574528222968563933317967414442817852555
[1]3191281372421239248353234135946434524615754563572
[1]3599124212461123532357223464346833457545794456865
[3]1254216394236532741534764385264587549637569865174
[1]2931385212314249632342535174345364628545647573965
[2]3119445813422155692453326671356443778246755488935
[2]2748628533385973964449618417555172952866628316397
[2]4924847833513595894462461691557357271266846838237
[324]76224394358733541546984465265719557637682166874
47[15]1426715826253782693736489371484759148259586125
857[4]5282229685639333179674144428178525553928963666
242[1]2392483532341359464345246157545635726865674683
246[1123532]3572234643468334575457944568656815567976
423653274[1]5347643852645875496375698651748671976285
231424963[2342]5351743453646285456475739656758684176
342215569245[332]66713564437782467554889357866599146
33859739644496[1]84175551729528666283163977739427418
35135958944624[61]6915573572712668468382377957949348
435873354154698[44]652657195576376821668748793277985
5826253782693736[4]893714847591482595861259361697236
9685639333179674[1]444281785255539289636664139174777
3532341359464345[2461]575456357268656746837976785794
3572234643468334575[4]579445686568155679767926678187
5347643852645875496[3]756986517486719762859782187396
3425351743453646285[4564]757396567586841767869795287
4533266713564437782467[554]8893578665991468977611257
449618417555172952866628[3163]9777394274188841538529
462461691557357271266846838[2]3779579493488168151459
546984465265719557637682166[8]7487932779859814388196
693736489371484759148259586[125]93616972361472718347
17967414442817852555392896366[6413]91747775241285888
46434524615754563572686567468379[7]67857948187896815
46833457545794456865681556797679[26]6781878137789298
645875496375698651748671976285978[21]873961893298417
4536462854564757396567586841767869[7]952878971816398
5644377824675548893578665991468977[6112]579188722368
5517295286662831639777394274188841538[5]299952649631
5735727126684683823779579493488168151[4]599279262561
6571955763768216687487932779859814388[1]961925499217
7148475914825958612593616972361472718[34725]83829458
28178525553928963666413917477752412858886[3]52396999
57545635726865674683797678579481878968159[2]98917926
57944568656815567976792667818781377892989[24]8891319
756986517486719762859782187396189329841729[1431]9528
564757396567586841767869795287897181639891829[2]7419
675548893578665991468977611257918872236812998[33479]

The total risk of this path is 315 (the starting position is still never entered, so its risk is not counted).

Using the full map, what is the lowest total risk of any path from the top left to the bottom right?
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

    def expand(self, times: int):
        """
        Expand the grid by the given number of times.

        The grid is expanded by adding new copies of the original grid
        to the right and downward of the original grid, multiplying the
        size of the grid in both dimensions. Each time the grid is copied,
        the risk levels are increased by 1 from the grid above or to the
        left of the copy. Risk levels above 9 loop back to 1.

        Args:
            times (int): The number of times to expand the grid
        """
        expanded_grid = [
            [None for _ in range(self.width * times)]
            for _ in range(self.height * times)
        ]
        for row in range(self.height * times):
            for col in range(self.width * times):
                cell_to_copy = self._grid[row % self.height][col % self.width]
                offset = row // self.height + col // self.width
                # risk loops around to 1 if it is greater than 9
                risk = (cell_to_copy.risk + offset - 1) % 9 + 1
                expanded_grid[row][col] = Tile(row, col, risk)
        self._grid = expanded_grid

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

    # the actual cave is 5 times expanded from the input
    risk_map.expand(5)

    print(risk_map.min_cost(risk_map[0, 0], risk_map[-1, -1]))


if __name__ == "__main__":
    main()
