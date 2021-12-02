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

# One-liner:
print((lambda d:sum((p[1]for p in d if p[0].startswith('f')))*sum((p[1]*sum((-dst if dir.startswith('u')else dst if dir.startswith('d')else 0 for(dir,dst)in d[:i]))for(i,p)in enumerate(d)if p[0].startswith('f'))))(tuple(map(lambda l:tuple(map(lambda s:int(s)if s.isnumeric()else s,l.split())),open('input.txt','r').readlines()))))