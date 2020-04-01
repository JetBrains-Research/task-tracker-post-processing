g4 = int(input())
g3 = []
g2 = 1
for g1 in range(g4):
    g3.append(int(input()))
for g0 in range(g4):
    if (g3[g0] == 0):
        g2 = 0
    if (g2 == 0):
        print('YES')
    else:
        print('NO')