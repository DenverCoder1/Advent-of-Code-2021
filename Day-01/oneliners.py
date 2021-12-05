# 1.1
print((lambda d: sum(int(d[i]) < int(d[i+1]) for i in range(len(d)-1)))(open("input.txt").readlines()))

# 1.2
print((lambda d: sum(sum(map(int, d[i:i+3])) < sum(map(int, d[i+1:i+4])) for i in range(len(d)-2)))(open("input.txt").readlines()))
