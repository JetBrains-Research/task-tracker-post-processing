a = int(input())
b = int(input())
c = int(input())
if ((a > b) and (a > c)):
    print(a)
elif ((b > a) and (b > c)):
    print(b)
elif ((c > a) and (c > b)):
    print(c)
elif ((c < b) and (c < a) and (a == b)):
    print(a)
elif ((c == b) and (a < c) and (a < b)):
    print(b)
elif (((b == c) and (b == a)) or ((c == a) and (b < c) and (b < a))):
    print(a)