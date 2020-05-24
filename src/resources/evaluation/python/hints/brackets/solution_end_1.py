s = input()

if len(s) <= 2:
    print(s)
else:
    for i, symb in enumerate(s):
        if i < len(s)//2:
            print(symb + '(', end='')



