a = int(input())
b = int(input())
c = int(input())
if (((c <= a) and (b <= a)) or ((c <= b) and (a <= b)) or ((b <= c) and (a <= c))):
    print(a)