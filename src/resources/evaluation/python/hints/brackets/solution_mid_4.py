# rate: 0
s = input()
res = ""
if len(s) % 2 == 0:
    for i in range(len(s) // 2):
        res += s[i] + "("
    for i in range(len(s) // 2 - 1, len(s)):
        res += s[i] + ")"