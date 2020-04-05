s = input()
length = len(s)
i = ''
if ((length % 2) == 0):
    for new_var_0 in range(((length // 2) - 1)):
        i = (i + (s[new_var_0] + '('))
    i = (i + (s[((length // 2) - 1)] + s[(length // 2)]))
    for new_var_0 in range(((length // 2) + 1), length):
        i = (i + (')' + s[new_var_0]))
    print(i)
else:
    for new_var_0 in range((length // 2)):
        i = (i + (s[new_var_0] + '('))
    i = (i + s[(length // 2)])
    for new_var_0 in range(((length // 2) + 1), length):
        i = (i + (')' + s[new_var_0]))
    print(i)