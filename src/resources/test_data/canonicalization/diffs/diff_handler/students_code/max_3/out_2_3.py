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
elif ((c < b) and (c < a) and (b == a)):
    print(a)
elif ((c == b) and (a < c) and (a < b)):
    print(b)
elif (((c == b) and (b == a)) or ((c == a) and (b < c) and (b < a))):
    print(a)