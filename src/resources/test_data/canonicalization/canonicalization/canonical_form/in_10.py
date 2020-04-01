# Replace -a + b < 5 to ((b - a) < 5). And rename variables
a = int(input())
b = int(input())
if -a + b < 5:
    print("YES")
else:
    print("NO")
