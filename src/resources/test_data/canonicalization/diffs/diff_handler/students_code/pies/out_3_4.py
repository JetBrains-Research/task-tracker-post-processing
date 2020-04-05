b = [0, 0]
n = int(input())
r = int(input())
c = int(input())
b[0] = (n * c)
b[1] = (r * c)
if (b[1] >= 100):
    b[0] = (b[0] + (b[1] // 100))
    b[1] = (b[1] % 100)
print(*b)