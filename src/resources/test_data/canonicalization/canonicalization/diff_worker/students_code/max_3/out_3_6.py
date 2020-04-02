a = int(input())
b = int(input())
c = int(input())
if ((a > b) and (a > c)):
    print(a)
elif ((b > a) and (b > c)):
    print(b)
elif ((c > a) and (c > b)):
    print(c)
elif (b == a):
    print(a, b)
elif (c == a):
    print(a, c)
elif (c == b):
    print(b, c)
elif ((c == b) and (b == a)):
    print(a, b, c)