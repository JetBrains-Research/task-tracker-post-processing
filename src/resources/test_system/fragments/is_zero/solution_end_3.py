N = int(input())
a = []
for i in range(N):
    c = int(input())
    a.append(c)
a.sort()
if a[0] != 0:
    print("NO")