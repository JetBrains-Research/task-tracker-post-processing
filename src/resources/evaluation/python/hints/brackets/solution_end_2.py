inp = input()
def func(l):
    if len(l) > 2:
        return l[0] + '(' + func(l[1:len(l) - 1]) + ')' + l[-1]
    return l
print('(' + func(inp) + ')')

