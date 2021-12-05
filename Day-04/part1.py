"""
--- Day 4: Giant Squid ---
You're already almost 1.5km (almost a mile) below the surface of the ocean, already so deep that you can't see any sunlight. What you can see, however, is a giant squid that has attached itself to the outside of your submarine.

Maybe it wants to play bingo?

Bingo is played on a set of boards each consisting of a 5x5 grid of numbers. Numbers are chosen at random, and the chosen number is marked on all boards on which it appears. (Numbers may not appear on all boards.) If all numbers in any row or any column of a board are marked, that board wins. (Diagonals don't count.)

The submarine has a bingo subsystem to help passengers (currently, you and the giant squid) pass the time. It automatically generates a random order in which to draw numbers and a random set of boards (your puzzle input). For example:

7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7

After the first five numbers are drawn (7, 4, 9, 5, and 11), there are no winners, but the boards are marked as follows (shown here adjacent to each other to save space):

22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
 8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
 6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
 1 12 20 15 19        14 21 16 12  6         2  0 12  3  7
After the next six numbers are drawn (17, 23, 2, 0, 14, and 21), there are still no winners:

22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
 8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
 6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
 1 12 20 15 19        14 21 16 12  6         2  0 12  3  7
Finally, 24 is drawn:

22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
 8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
 6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
 1 12 20 15 19        14 21 16 12  6         2  0 12  3  7
At this point, the third board wins because it has at least one complete row or column of marked numbers (in this case, the entire top row is marked: 14 21 17 24 4).

The score of the winning board can now be calculated. Start by finding the sum of all unmarked numbers on that board; in this case, the sum is 188. Then, multiply that sum by the number that was just called when the board won, 24, to get the final score, 188 * 24 = 4512.

To guarantee victory against the giant squid, figure out which board will win first. What will your final score be if you choose that board?
"""


class Board:
    def __init__(self, grid: list[list[int]]):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])
        self.marked = [[False for _ in range(self.cols)] for _ in range(self.rows)]

    def mark_number(self, number: int):
        """
        Mark all cells with the given number

        Args:
            number(int): number to mark
        """
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col] == number:
                    self.mark_cell(row, col)

    def mark_cell(self, row: int, col: int):
        """
        Mark a cell given its row and column

        Args:
            row(int): row of the cell
            col(int): column of the cell
        """
        self.marked[row][col] = True

    def has_won(self) -> bool:
        """
        Check if any row or column is completely marked

        Returns:
            bool: True if any row or column is completely marked
        """
        return any(
            all(self.marked[row][col] for col in range(self.cols))
            for row in range(self.rows)
        ) or any(
            all(self.marked[col][row] for col in range(self.cols))
            for row in range(self.rows)
        )

    def sum_unmarked(self) -> int:
        """
        Sum all unmarked numbers

        Returns:
            int: sum of all unmarked numbers
        """
        return sum(
            sum(
                self.grid[row][col]
                for col in range(self.cols)
                if not self.marked[row][col]
            )
            for row in range(self.rows)
        )

    def __repr__(self) -> str:
        """
        Pad each cell to length 2 with spaces (aligned right)
        Place an X instead of the number for marked cells
        Add a newline after each

        Example:
         X 99  X  X  X
         X 30 10  X  X
        98  X  X  X 25
        76  X 29  X  X
         X  X  X  X  X
        """
        return "\n".join(
            [
                " ".join(
                    [
                        (
                            "X" if self.marked[row][col] else str(self.grid[row][col])
                        ).rjust(2)
                        for col in range(self.cols)
                    ]
                )
                for row in range(self.rows)
            ]
        )

    @classmethod
    def from_lines(cls, lines: list[str]):
        """
        Create a board from a list of lines where each line is a list of numbers separated by spaces.
        Each line represents a row of the board.
        """
        grid = [[int(x) for x in line.split()] for line in lines]
        return cls(grid)


if __name__ == "__main__":
    with open("input.txt") as f:
        data = f.read().splitlines()

    drawn_numbers = data[0].split(",")

    boards = [Board.from_lines(data[i + 1 : i + 6]) for i in range(1, len(data), 6)]

    for number in drawn_numbers:
        for board in boards:
            board.mark_number(int(number))
            if board.has_won():
                print(f"{number} wins")
                print(board)
                print(f"score: {board.sum_unmarked() * int(number)}")
                exit()
