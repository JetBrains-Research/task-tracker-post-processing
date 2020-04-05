N = int(input())
i = [int(new_var_0) for new_var_0 in input().split()]
s = 0
i = sorted(i)
while ((s > N) and (i[s] != 0) and (i[s] < 1)):
    s = (s + 1)
if (i[s] == 0):
    print('YES')
else:
    print('NO')