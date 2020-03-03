g2 = int(input())
g1 = 0
for g0 in range(g2):
    g3 = int(input())
    if (g3 == 0):
        g1 += 1
if (g1 == 0):
    print('NO')
else:
    print('YES')