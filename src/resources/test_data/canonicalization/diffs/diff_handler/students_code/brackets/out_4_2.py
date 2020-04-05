l = input()
s1 = len(l)
print(l[0], end='')
for s2 in range(1, ((s1 // 2) + (s1 % 2))):
    print(('(' + l[s2]), end='')
if ((s1 % 2) == 1):
    for s2 in range(((s1 // 2) + (s1 % 2)), len(l)):
        print((')' + l[s2]), end='')
else:
    for s2 in range((s1 // 2), (s1 - 1)):
        print((l[s2] + ')'), end='')
    print(l[(len(l) - 1)])