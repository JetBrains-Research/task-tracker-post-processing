a = int(input())
c = 0
for n in range(a):
    b = int(input())
    if (b == 0):
        c = (c + 1)
if (c == 0):
    print('NO')
else:
    print('YES')