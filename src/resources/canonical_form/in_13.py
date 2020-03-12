# Replace a > b or (c <= a and b <= a) to ((b < a) or ((c <= a) and (b <= a))) and rename it
a = int(input())
b = int(input())
c = int(input())
if a > b or (c <= a and b <= a):
    print("YES")
else:
    print("NO")
