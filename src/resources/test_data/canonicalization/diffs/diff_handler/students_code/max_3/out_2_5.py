a = int(input())
b = int(input())
c = int(input())
if ((a > b) and (b > c)):
    print(a)
elif ((a > c) and (c > b)):
    print(a)
elif ((b > c) and (c > a)):
    print(b)
elif ((b > a) and (a > c)):
    print(b)
elif ((c > b) and (b > a)):
    print(c)
elif ((c > a) and (a > b)):
    print(c)