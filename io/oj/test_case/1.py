f = list()
f.append(0)
f.append(1)
f.append(2)
f.append(4)

for _ in range(100):
    f.append(f[-1]+f[-2]+f[-3])

n = int(raw_input())
print f[n]
