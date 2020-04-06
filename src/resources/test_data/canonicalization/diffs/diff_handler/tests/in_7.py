def addition(n):
    return n + n


numbers = [1, 2, 3, 4]
result = map(addition, numbers)
print(list(result))