new_var_0 = int(input())
cost = int(input())
a = int(input())
b = (new_var_0 * a)
n = (cost * a)
while (n >= 100):
    b = (b + 1)
    n = (n - 100)
print(b, n)