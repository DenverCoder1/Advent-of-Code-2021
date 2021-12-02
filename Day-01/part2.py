with open("input.txt", "r") as f:
    data = f.readlines()

# sums of each group of three depths
threes = [sum(map(int, data[i : i + 3])) for i in range(len(data) - 2)]

# count the number of times the sum of the group of three increases
print(sum(1 for i in range(len(threes) - 1) if int(threes[i]) < int(threes[i + 1])))
