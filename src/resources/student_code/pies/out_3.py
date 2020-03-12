g4 = int(input())
g3 = int(input())
g2 = int(input())
g1 = (g2 * g4)
g0 = (g2 * g3)
while (100 <= g0):
    g1 = (g1 + 1)
    g0 = (g0 - 100)
print(g1, g0)