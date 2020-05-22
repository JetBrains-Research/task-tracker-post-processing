a = int(input())
b = int(input())
n = int(input())
rub = a * n
if b * n >= 100:
    rub += b * n // 100
    cop = b * n
    print(rub + " " + cop)