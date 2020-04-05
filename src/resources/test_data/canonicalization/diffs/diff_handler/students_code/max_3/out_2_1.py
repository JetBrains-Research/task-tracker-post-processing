a = int(input())
b = int(input())
c = int(input())
if (b < a):
    max = a
else:
    max = b
if (b > c):
    max = b
if (max < c):
    max = c
print(max)