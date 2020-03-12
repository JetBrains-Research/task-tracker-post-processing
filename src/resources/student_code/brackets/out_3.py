g0 = input()
if (2 < len(g0)):
    if ((len(g0) % 2) == 0):
        g0 = ('('.join(g0[:int((len(g0) / 2))]) + ')'.join(g0[int((len(g0) / 2)):]))
    else:
        g0 = (('('.join(g0[:(int((len(g0) / 2)) + 1)]) + ')') + ')'.join(g0[int(((len(g0) / 2) + 1)):]))
print(g0)