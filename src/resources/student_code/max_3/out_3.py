g2 = int(input())
g1 = int(input())
g0 = int(input())
if (((g0 <= g1) and (g2 <= g1)) or ((g0 <= g2) and (g1 <= g2)) or ((g1 <= g0) and (g2 <= g0))):
    print(g2)