# rate: 0
n = int(input())
fib = []
while len(fib) < n:
    if len(fib) < 2:
        fib.append(1)
    else:
        fib.append(fib[-2] + fib[-1])
print(fib)


