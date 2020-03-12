g4 = int(input())
g3 = int(input())
g2 = int(input())
g1 = []
g0 = []
if (g4 == 1):
    g0.append(g4)
else:
    g1.append(g4)
if (g3 == 1):
    g0.append(g3)
else:
    g1.append(g3)
if (g2 == 1):
    g0.append(g2)
else:
    g1.append(g2)
if (len(g1) < len(g0)):
    print(1)
elif (len(g0) < len(g1)):
    print(0)