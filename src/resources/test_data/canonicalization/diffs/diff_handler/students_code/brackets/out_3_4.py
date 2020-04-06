new_var_0 = input()
new_var_1 = len(new_var_0)
new_var_2 = new_var_0[:(new_var_1 // 2)]
s = new_var_0[((new_var_1 + 1) // 2):]
print('('.join(new_var_2), end='')
if ((new_var_1 % 2) == 1):
    new_var_3 = new_var_0[(new_var_1 // 2)]
    if (new_var_1 > 1):
        new_var_3 = (('(' + new_var_3) + ')')
    print(new_var_3, sep='', end='')
print(')'.join(s))