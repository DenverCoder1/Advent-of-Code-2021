with open("input.txt", "r") as f:
    data = f.readlines()

print(sum(1 for i in range(len(data)-1) if int(data[i]) < int(data[i+1])))

# One-liner:
print((lambda d: sum(1 for i in range(len(d)-1) if int(d[i]) < int(d[i+1])))(open("input.txt", "r").readlines()))