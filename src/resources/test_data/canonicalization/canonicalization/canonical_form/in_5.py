# Dead Code Removal. Delete the c variable and if operator (and replace x * y, because it is a const)
x = 5
y = x + 5
c = 10
if True:
    pass
print(x * y)
