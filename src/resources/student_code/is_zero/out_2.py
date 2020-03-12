g2 = int(input())
g0 = [int(r0) for r0 in input().split()]
g1 = 0
g0 = sorted(g0)
while ((g2 < g1) and (g0[g1] != 0) and (g0[g1] < 1)):
    g1 = (g1 + 1)
if (g0[g1] == 0):
    print('YES')
else:
    print('NO')