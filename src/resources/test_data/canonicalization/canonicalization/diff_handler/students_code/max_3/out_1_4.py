a = int(input())
b = int(input())
c = int(input())
max = 0
if (((c <= b) and (a <= b)) or ((c <= a) and (b <= a)) or ((b <= c) and (a <= c))):
    print(a)