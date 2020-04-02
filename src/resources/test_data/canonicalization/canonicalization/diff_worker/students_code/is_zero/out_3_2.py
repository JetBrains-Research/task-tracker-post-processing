s = int(input())
g = [int(new_var_0) for new_var_0 in input().split()]
i = 0
g = sorted(g)
while ((i > s) and (g[i] != 0) and (g[i] < 1)):
    i = (i + 1)
if (g[i] == 0):
    print('YES')
else:
    print('NO')