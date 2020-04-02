x = int(input())
y = int(input())
z = int(input())
if (y < x):
    max = x
else:
    max = y
if (z < y):
    max = y
if (max < z):
    max = z
print(max)