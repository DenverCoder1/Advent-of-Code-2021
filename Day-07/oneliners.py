# 7.1
print((lambda data: sum(abs(int(__import__("statistics").median(data)) - position) for position in data))([int(x) for x in open("input.txt").read().split(",")]))

# 7.2
print((lambda data: (target := sum(data) // len(data)) and sum(abs(target - position) * (abs(target - position) + 1) // 2 for position in data))([int(x) for x in open("input.txt").read().split(",")]))