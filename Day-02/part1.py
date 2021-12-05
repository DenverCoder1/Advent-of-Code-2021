"""
--- Day 2: Dive! ---
Now, you need to figure out how to pilot this thing.

It seems like the submarine can take a series of commands like forward 1, down 2, or up 3:

forward X increases the horizontal position by X units.
down X increases the depth by X units.
up X decreases the depth by X units.
Note that since you're on a submarine, down and up affect your depth, and so they have the opposite result of what you might expect.

The submarine seems to already have a planned course (your puzzle input). You should probably figure out where it's going. For example:

forward 5
down 5
forward 8
up 3
down 8
forward 2

Your horizontal position and depth both start at 0. The steps above would then modify them as follows:

forward 5 adds 5 to your horizontal position, a total of 5.
down 5 adds 5 to your depth, resulting in a value of 5.
forward 8 adds 8 to your horizontal position, a total of 13.
up 3 decreases your depth by 3, resulting in a value of 2.
down 8 adds 8 to your depth, resulting in a value of 10.
forward 2 adds 2 to your horizontal position, a total of 15.
After following these instructions, you would have a horizontal position of 15 and a depth of 10. (Multiplying these together produces 150.)

Calculate the horizontal position and depth you would have after following the planned course. What do you get if you multiply your final horizontal position by your final depth?
"""


class Position:
    """
    Class to represent the position of the submarine
    """

    def __init__(self, horizontal: int, depth: int):
        self.horizontal = horizontal
        self.depth = depth

    def execute(self, instruction: str):
        """
        Execute an instruction on the position in the form "direction distance"

        Args:
            instruction (str): instruction to execute
        """
        direction, distance = instruction.split(" ")
        distance = int(distance)
        if direction == "forward":
            self.move_forward(distance)
        elif direction == "up":
            self.move_up(distance)
        else:
            assert direction == "down"
            self.move_down(distance)

    def move_forward(self, distance: int):
        """
        Move forward a given distance

        Args:
            distance (int): distance to move
        """
        self.horizontal += distance

    def move_up(self, distance: int):
        """
        Move up a given distance, decreasing the depth

        Args:
            distance (int): distance to move
        """
        self.depth -= distance

    def move_down(self, distance: int):
        """
        Move down a given distance, increasing the depth

        Args:
            distance (int): distance to move
        """
        self.depth += distance


def travel(instructions: list[str]) -> int:
    """
    Executes the instructions and returns the horizontal distance times the depth

    Args:
        instructions (list[str]): instructions to execute

    Returns:
        int: horizontal distance times the depth
    """
    position = Position(0, 0)

    for instruction in instructions:
        position.execute(instruction)

    return position.horizontal * position.depth


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        instructions = f.readlines()
    print(travel(instructions))
