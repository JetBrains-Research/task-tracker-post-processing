l = input()
s1 = len(l)
s2 = ''
if ((s1 % 2) == 0):
    for s in range(((s1 // 2) - 1)):
        s2 = (s2 + (l[s] + '('))
    s2 = (s2 + (l[((s1 // 2) - 1)] + l[(s1 // 2)]))
    for s in range(((s1 // 2) + 1), s1):
        s2 = (s2 + (')' + l[s]))
    print(s2)
else:
    for s in range((s1 // 2)):
        s2 = (s2 + (l[s] + '('))
    s2 = (s2 + l[(s1 // 2)])
    for s in range(((s1 // 2) + 1), s1):
        s2 = (s2 + (')' + l[s]))
    print(s2)