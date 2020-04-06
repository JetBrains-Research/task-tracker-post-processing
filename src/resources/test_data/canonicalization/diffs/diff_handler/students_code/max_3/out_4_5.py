a = int(input())
b = int(input())
c = int(input())
if ((c < b) and (b < a)):
    print(a)
elif ((c < a) and (b < c)):
    print(a)
elif ((c < b) and (a < c)):
    print(b)
elif ((c < a) and (a < b)):
    print(b)
elif (((b < c) and (a < b)) or ((b < a) and (a < c))):
    print(c)