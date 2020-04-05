s2 = input()
if (len(s2) > 2):
    if ((len(s2) % 2) == 0):
        s2 = ('('.join(s2[:int((len(s2) / 2))]) + ')'.join(s2[int((len(s2) / 2)):]))
    else:
        s2 = (('('.join(s2[:(int((len(s2) / 2)) + 1)]) + ')') + ')'.join(s2[int(((len(s2) / 2) + 1)):]))
print(s2)