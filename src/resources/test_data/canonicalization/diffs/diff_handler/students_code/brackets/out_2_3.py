i = input()
if (len(i) > 2):
    if ((len(i) % 2) == 0):
        i = ('('.join(i[:int((len(i) / 2))]) + ')'.join(i[int((len(i) / 2)):]))
    else:
        i = (('('.join(i[:(int((len(i) / 2)) + 1)]) + ')') + ')'.join(i[int(((len(i) / 2) + 1)):]))
print(i)