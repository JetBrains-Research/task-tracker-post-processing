new_var_0 = input()
new_var_1 = len(new_var_0)
print(new_var_0[0], end='')
for s in range(1, ((new_var_1 // 2) + (new_var_1 % 2))):
    print(('(' + new_var_0[s]), end='')
if ((new_var_1 % 2) == 1):
    for s in range(((new_var_1 // 2) + (new_var_1 % 2)), len(new_var_0)):
        print((')' + new_var_0[s]), end='')
else:
    for s in range((new_var_1 // 2), (new_var_1 - 1)):
        print((new_var_0[s] + ')'), end='')
    print(new_var_0[(len(new_var_0) - 1)])