# 7.1
print((lambda data: min(sum(abs(target - position) for position in data) for target in range(max(data))))([int(x) for x in open("input.txt").read().split(",")]))

# 7.2
print((lambda data: min(sum(abs(target - position) * (abs(target - position) + 1) // 2 for position in data) for target in range(max(data))))([int(x) for x in open("input.txt").read().split(",")]))