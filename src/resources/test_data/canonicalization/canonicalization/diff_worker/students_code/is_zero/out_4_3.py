new_var_0 = int(input())
b = []
a = 1
for c in range(new_var_0):
    b.append(int(input()))
for n in range(new_var_0):
    if (b[n] == 0):
        a = 0
    if (a == 0):
        print('YES')
    else:
        print('NO')