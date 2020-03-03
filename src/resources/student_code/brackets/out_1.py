g2 = input()
g1 = len(g2)
g0 = ''
if ((g1 % 2) == 0):
    for g3 in range(((g1 // 2) - 1)):
        g0 += (g2[g3] + '(')
    g0 += (g2[((g1 // 2) - 1)] + g2[(g1 // 2)])
    for g3 in range(((g1 // 2) + 1), g1):
        g0 += (')' + g2[g3])
    print(g0)
else:
    for g3 in range((g1 // 2)):
        g0 += (g2[g3] + '(')
    g0 += g2[(g1 // 2)]
    for g3 in range(((g1 // 2) + 1), g1):
        g0 += (')' + g2[g3])
    print(g0)