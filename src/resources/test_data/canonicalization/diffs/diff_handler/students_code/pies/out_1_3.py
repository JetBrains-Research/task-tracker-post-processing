b = int(input())
n = int(input())
h = 0
new_var_0 = int(input())
kop = (new_var_0 * n)
rub = (b * new_var_0)
while (100 <= kop):
    rub = (rub + 1)
    kop = (kop - 100)
print(rub, kop)