# rate: 0
n = int(input())
factorial_list = []
while n > 0:
    factorial_list.append(1)
    factorial_list = [n*f for f in factorial_list]
    n -= 1
print(factorial_list)

