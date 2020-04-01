(r0, r1, r2) = map(int, input().split())
if ((r0 == r1) and (r1 == 1)):
    print(1)
elif ((r0 == r2) and (r2 == 1)):
    print(1)
elif ((r1 == r2) and (r1 == 1)):
    print(1)
elif ((r0 == r2) and (r0 == r1) and (r1 == 1)):
    print(1)
else:
    print(0)
