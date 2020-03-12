g2 = input()
g1 = len(g2)
print(g2[0], end='')
for g0 in range(1, ((g1 % 2) + (g1 // 2))):
    print(('(' + g2[g0]), end='')
if ((g1 % 2) == 1):
    for g0 in range(((g1 % 2) + (g1 // 2)), len(g2)):
        print((')' + g2[g0]), end='')
else:
    for g0 in range((g1 // 2), (g1 - 1)):
        print((g2[g0] + ')'), end='')
    print(g2[(len(g2) - 1)])