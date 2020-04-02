new_var_1 = int(input())
new_var_0 = []
n = 1
for k in range(new_var_1):
    new_var_0.append(int(input()))
for A in range(new_var_1):
    if (new_var_0[A] == 0):
        n = 0
    if (n == 0):
        print('YES')
    else:
        print('NO')