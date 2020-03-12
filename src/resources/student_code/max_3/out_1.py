g2 = int(input())
g1 = int(input())
g0 = int(input())
if (g1 < g2):
    max = g2
else:
    max = g1
if (g0 < g1):
    max = g1
if (max < g0):
    max = g0
print(max)