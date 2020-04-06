a = int(input())
n = [int(new_var_0) for new_var_0 in input().split()]
c = 0
n = sorted(n)
while ((c > a) and (n[c] != 0) and (n[c] < 1)):
    c = (c + 1)
if (n[c] == 0):
    print('YES')
else:
    print('NO')