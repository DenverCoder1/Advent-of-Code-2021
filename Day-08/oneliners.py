# 8.1
print((data := open("input.txt").read().splitlines()) and sum(sum(len(d) in (2, 3, 4, 7) for d in line.split(" | ")[1].split(" ")) for line in data))
