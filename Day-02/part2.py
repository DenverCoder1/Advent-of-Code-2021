"""
--- Part Two ---
Based on your calculations, the planned course doesn't seem to make any sense. You find the submarine manual and discover that the process is actually slightly more complicated.

In addition to horizontal position and depth, you'll also need to track a third value, aim, which also starts at 0. The commands also mean something entirely different than you first thought:

down X increases your aim by X units.
up X decreases your aim by X units.
forward X does two things:
It increases your horizontal position by X units.
It increases your depth by your aim multiplied by X.

Again note that since you're on a submarine, down and up do the opposite of what you might expect: "down" means aiming in the positive direction.

Now, the above example does something different:

forward 5 adds 5 to your horizontal position, a total of 5. Because your aim is 0, your depth does not change.
down 5 adds 5 to your aim, resulting in a value of 5.
forward 8 adds 8 to your horizontal position, a total of 13. Because your aim is 5, your depth increases by 8*5=40.
up 3 decreases your aim by 3, resulting in a value of 2.
down 8 adds 8 to your aim, resulting in a value of 10.
forward 2 adds 2 to your horizontal position, a total of 15. Because your aim is 10, your depth increases by 2*10=20 to a total of 60.

After following these new instructions, you would have a horizontal position of 15 and a depth of 60. (Multiplying these produces 900.)

Using this new interpretation of the commands, calculate the horizontal position and depth you would have after following the planned course. What do you get if you multiply your final horizontal position by your final depth?
"""


class Position:
    """
    Class to represent the position of the submarine
    """

    def __init__(self, horizontal: int, depth: int, aim: int):
        self.horizontal = horizontal
        self.depth = depth
        self.aim = aim

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
        self.depth += self.aim * distance

    def move_up(self, distance: int):
        """
        Move up a given distance, decreasing the aim

        Args:
            distance (int): distance to move
        """
        self.aim -= distance

    def move_down(self, distance: int):
        """
        Move down a given distance, increasing the aim

        Args:
            distance (int): distance to move
        """
        self.aim += distance


def travel(instructions: list[str]) -> int:
    """
    Executes the instructions and returns the horizontal distance times the depth

    Args:
        instructions (list[str]): instructions to execute

    Returns:
        int: horizontal distance times the depth
    """
    position = Position(0, 0, 0)

    for instruction in instructions:
        position.execute(instruction)

    return position.horizontal * position.depth


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        instructions = f.readlines()
    print(travel(instructions))
