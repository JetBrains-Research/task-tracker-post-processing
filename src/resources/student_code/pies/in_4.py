cost = [0, 0]
a = int(input()) #Ã°Ã³Ã¡
b = int(input()) #ÃªÃ®Ã¯
n = int(input()) #ÃªÃ®Ã«-Ã¢Ã®
cost[0] = a * n
cost[1] = b * n
if cost[1] >= 100:
    cost[0] += cost[1] // 100
    cost[1] = cost[1] % 100
print(*cost)