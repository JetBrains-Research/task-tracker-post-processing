n = int(input())
k = 0
for A in range(n):
    new_var_0 = int(input())
    if (new_var_0 == 0):
        k = (k + 1)
if (k == 0):
    print('NO')
else:
    print('YES')