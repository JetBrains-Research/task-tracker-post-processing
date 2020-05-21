a = int(input())
b = int(input())
c = int(input())
if a > b and a > c:
    print(a)
elif a == b == c:
    print(a)
elif b > a and b < c:
    print(c)