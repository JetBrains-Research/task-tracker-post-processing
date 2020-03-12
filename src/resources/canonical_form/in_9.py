# Replace -a + b > 5 to (5 < (b - a)) and change > to <. And rename variables
a = int(input())
b = int(input())
if -a + b > 5:
    print("YES")
else:
    print("NO")
