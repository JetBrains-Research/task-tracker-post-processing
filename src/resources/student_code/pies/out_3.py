g4 = int(input())
g3 = int(input())
g2 = int(input())
g1 = (g4 * g2)
g0 = (g3 * g2)
while (100 <= g0):
    g1 += 1
    g0 -= 100
print(g1, g0)