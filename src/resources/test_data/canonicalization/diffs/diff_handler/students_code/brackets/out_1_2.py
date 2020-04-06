s = input()
n = len(s)
print(s[0], end='')
for ans in range(1, ((n // 2) + (n % 2))):
    print(('(' + s[ans]), end='')
if ((n % 2) == 1):
    for ans in range(((n // 2) + (n % 2)), len(s)):
        print((')' + s[ans]), end='')
else:
    for ans in range((n // 2), (n - 1)):
        print((s[ans] + ')'), end='')
    print(s[(len(s) - 1)])