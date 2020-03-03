g2 = int(input())
g1 = int(input())
g0 = int(input())
if ((g1 < g2) and (g0 < g2)):
    print(g2)
if ((g2 < g1) and (g0 < g1)):
    print(g1)
if ((g2 < g0) and (g1 < g0)):
    print(g0)
if (((g1 < g2) and (g2 == g0)) or ((g0 < g2) and (g2 == g1))):
    print(g2)
if (((g2 < g1) and (g1 == g0)) or ((g0 < g1) and (g2 == g1))):
    print(g1)
if ((g1 < g0) or ((g2 < g0) and (g1 == g0))):
    print(g0)