a = int(input())
b = int(input())
c = int(input())
if (a > c):
    if (a > b):
        print(a)
elif ((c < b) and (a < b)):
    print(b)
elif ((b < c) and (a < c)):
    print(c)
elif (b == a):
    print(a, b)
elif (c == a):
    print(a, c)
elif (c == b):
    print(b, c)
elif ((c == b) and (b == a)):
    print(a, b, c)