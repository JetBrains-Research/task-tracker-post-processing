g1 = str(input())
max = '0'
for g0 in g1:
    if g0.isdigit():
        int(g0)
        if (max < g0):
            max = g0
print(max)