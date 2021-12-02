class Position:
    """
    Class to represent the position of the submarine
    """

    def __init__(self, horizontal: int, depth: int):
        self.horizontal = horizontal
        self.depth = depth

    def move(self, instruction: str):
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


def travel(data: list[str]) -> int:
    """
    Executes the instructions and returns the horizontal distance times the depth

    Args:
        data (list[str]): instructions to execute

    Returns:
        int: horizontal distance times the depth
    """
    position = Position(0, 0)

    for instruction in data:
        position.move(instruction)

    return position.horizontal * position.depth


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        data = f.readlines()
    print(travel(data))
