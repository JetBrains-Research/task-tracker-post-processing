# Replace -b - a < 5 to (((- b) - a) < 5) and rename it
a = int(input())
b = int(input())
if -b - a < 5:
    print("YES")
else:
    print("NO")
