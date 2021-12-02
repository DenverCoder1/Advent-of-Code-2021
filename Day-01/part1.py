with open("input.txt", "r") as f:
    data = f.readlines()

print(sum(1 for i in range(len(data) - 1) if int(data[i]) < int(data[i + 1])))
