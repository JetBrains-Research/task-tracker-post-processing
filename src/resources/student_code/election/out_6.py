g2 = int(input())
g1 = int(input())
g0 = int(input())
if (((g0 == g1) and (g1 == g2)) or ((g0 != g1) and (g1 == g2))):
    if (g2 == 1):
        print(1)
    else:
        print(0)
if (((g0 == g1) and (g1 == g2)) or ((g0 == g2) and (g0 != g1))):
    if (g2 == 1):
        print(1)
    else:
        print(0)
if (((g0 == g1) and (g1 == g2)) or ((g0 == g2) and (g0 != g1))):
    if (g2 == 1):
        print(1)
    else:
        print(0)