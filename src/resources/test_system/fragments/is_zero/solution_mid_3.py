N = int(input())
c = 0
for i in range(N):
    a = int(input())
    if a == 0:
        c += 1
if c > 0:
    print("YES")