# 1.1
print((lambda d: sum(1 for i in range(len(d)-1) if int(d[i]) < int(d[i+1])))(open("input.txt", "r").readlines()))

# 1.2
print((lambda d: sum(1 for i in range(len(d)-2) if sum(map(int, d[i:i+3])) < sum(map(int, d[i+1:i+4]))))(open("input.txt", "r").readlines()))
