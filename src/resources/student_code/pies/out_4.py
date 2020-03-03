g3 = [0, 0]
g2 = int(input())
g1 = int(input())
g0 = int(input())
g3[0] = (g2 * g0)
g3[1] = (g1 * g0)
if (100 <= g3[1]):
    g3[0] += (g3[1] // 100)
    g3[1] = (g3[1] % 100)
print(*g3)