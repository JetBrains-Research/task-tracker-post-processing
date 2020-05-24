# rate: 0.125
s = input()
res = ""
if len(s) < 2:
    print(s)
elif len(s) == 3:
    print(s[0] + '(' + s[1] + ')' + s[2])
elif len(s) == 4:
    print(s[0] + '(' + s[1:3] + ')' + s[3])
