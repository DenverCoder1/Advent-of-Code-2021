# 2.1
print((lambda d: sum(map(int, [step.split(" ")[1] for step in d if step.startswith("f")])) * (sum(map(int, [step.split(" ")[1] for step in d if step.startswith("d")])) - sum(map(int, [step.split(" ")[1] for step in d if step.startswith("u")]))))(open("input.txt", "r").readlines()))

# 2.2
print((lambda d: sum((p[1] for p in d if p[0].startswith('f')))*sum((p[1]*sum((-dst if dir.startswith('u')else dst if dir.startswith('d') else 0 for(dir,dst)in d[:i]))for(i,p)in enumerate(d)if p[0].startswith('f'))))(tuple(map(lambda l:tuple(map(lambda s:int(s)if s.isnumeric()else s,l.split())),open('input.txt','r').readlines()))))
