with open("input.txt", "r") as f:
    data = f.readlines()


class Position:
    def __init__(self, horizontal, depth, aim):
        self.horizontal = horizontal
        self.depth = depth
        self.aim = aim


position = Position(0, 0, 0)

for step in data:
    direction, distance = step.split(" ")
    distance = int(distance)
    if direction == "forward":
        position.horizontal += distance
        position.depth += position.aim * distance
    elif direction == "up":
        position.aim -= distance
    elif direction == "down":
        position.aim += distance

print(position.horizontal * position.depth)