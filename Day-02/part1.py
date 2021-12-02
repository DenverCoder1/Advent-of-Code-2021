with open("input.txt", "r") as f:
    data = f.readlines()


class Position:
    def __init__(self, horizontal, depth):
        self.horizontal = horizontal
        self.depth = depth


position = Position(0, 0)

for step in data:
    direction, distance = step.split()
    distance = int(distance)

    if direction == "forward":
        position.horizontal += distance
    elif direction == "up":
        position.depth -= distance
    elif direction == "down":
        position.depth += distance

print(position.horizontal * position.depth)

# One-liner:
print((lambda d: sum(map(int, [step.split(" ")[1] for step in d if step.startswith("f")])) * (sum(map(int, [step.split(" ")[1] for step in d if step.startswith("d")])) - sum(map(int, [step.split(" ")[1] for step in d if step.startswith("u")]))))(open("input.txt", "r").readlines()))
