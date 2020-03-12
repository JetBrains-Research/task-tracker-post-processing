g3 = input()
g2 = len(g3)
g1 = g3[:(g2 // 2)]
g0 = g3[((g2 + 1) // 2):]
print('('.join(g1), end='')
if ((g2 % 2) == 1):
    g4 = g3[(g2 // 2)]
    if (1 < g2):
        g4 = (('(' + g4) + ')')
    print(g4, sep='', end='')
print(')'.join(g0))