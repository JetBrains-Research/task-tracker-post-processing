g4 = int(input())
g3 = int(input())
g2 = int(input())
g1 = (g4 * g2)
g0 = (g3 * g2)
if (100 <= g0):
    g5 = (g0 // 100)
    g0 = (g0 % 100)
    g1 += g5
print(g1, end=' ')
print(g0)