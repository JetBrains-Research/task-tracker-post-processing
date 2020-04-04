a = int(input())
b = int(input())
c = int(input())
if ((a > b) and (b > c)):
    print(a)
elif ((c > b) and (a > c)):
    print(a)
elif ((c > a) and (b > c)):
    print(b)
elif ((b > a) and (a > c)):
    print(b)
elif (((b < c) and (a < b)) or ((b < a) and (c > a))):
    print(c)