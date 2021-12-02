with open("input.txt", "r") as f:
    data = f.readlines()

sum_threes = [sum(map(int, data[i:i+3])) for i in range(len(data)-2)]
print(sum(1 for i in range(len(sum_threes)-1) if int(sum_threes[i]) < int(sum_threes[i+1])))

# One-liner:
print((lambda x: sum(1 for i in range(len(x)-2) if sum(map(int, x[i:i+3])) < sum(map(int, x[i+1:i+4]))))(open("input.txt", "r").readlines()))