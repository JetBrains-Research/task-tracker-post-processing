new_var_0 = int(input())
a = []
N = 1
for s in range(new_var_0):
    a.append(int(input()))
for i in range(new_var_0):
    if (a[i] == 0):
        N = 0
    if (N == 0):
        print('YES')
    else:
        print('NO')