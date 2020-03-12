g6 = int(input())
g5 = int(input())
g4 = int(input())
g3 = []
g2 = []
if (g6 == 1):
    g2.append(g6)
else:
    g3.append(g6)
if (g5 == 1):
    g2.append(g5)
else:
    g3.append(g5)
if (g4 == 1):
    g2.append(g4)
else:
    g3.append(g4)
if (len(g3) < len(g2)):
    print(1)
elif (len(g2) < len(g3)):
    print(0)