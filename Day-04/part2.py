"""
--- Part Two ---
On the other hand, it might be wise to try a different strategy: let the giant squid win.

You aren't sure how many bingo boards a giant squid could play at once, so rather than waste time counting its arms, the safe thing to do is to figure out which board will win last and choose that one. That way, no matter which boards it picks, it will win for sure.

In the above example, the second board is the last to win, which happens after 13 is eventually called and its middle column is completely marked. If you were to keep playing until this point, the second board would have a sum of unmarked numbers equal to 148 for a final score of 148 * 13 = 1924.

Figure out which board will win last. Once it wins, what would its final score be?
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
            all(self.marked[row][col] for row in range(self.rows))
            for col in range(self.cols)
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

    boards_won = [False for _ in range(len(boards))]

    for number in drawn_numbers:
        for i, board in enumerate(boards):
            board.mark_number(int(number))
            if board.has_won():
                boards_won[i] = True
                if all(boards_won):
                    print(f"{number} wins")
                    print(board)
                    print(f"score: {board.sum_unmarked() * int(number)}")
                    exit()
