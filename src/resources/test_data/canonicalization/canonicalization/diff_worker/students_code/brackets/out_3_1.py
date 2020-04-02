new_var_1 = input()
s = ''
new_var_0 = len(new_var_1)
if ((new_var_0 % 2) == 0):
    for new_var_2 in range(((new_var_0 // 2) - 1)):
        s = (s + (new_var_1[new_var_2] + '('))
    s = (s + (new_var_1[((new_var_0 // 2) - 1)] + new_var_1[(new_var_0 // 2)]))
    for new_var_2 in range(((new_var_0 // 2) + 1), new_var_0):
        s = (s + (')' + new_var_1[new_var_2]))
    print(s)
else:
    for new_var_2 in range((new_var_0 // 2)):
        s = (s + (new_var_1[new_var_2] + '('))
    s = (s + new_var_1[(new_var_0 // 2)])
    for new_var_2 in range(((new_var_0 // 2) + 1), new_var_0):
        s = (s + (')' + new_var_1[new_var_2]))
    print(s)