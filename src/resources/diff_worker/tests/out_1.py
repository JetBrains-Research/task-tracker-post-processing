a = int(input())
b = int(input())
n = int(input())
res = (a * 100 * n + b * n) // 100
print(str(res) + " " + str((a * 100 * n + b * n) % 100))
