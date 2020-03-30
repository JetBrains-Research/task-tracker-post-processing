a_1 = int(input())
b_1 = int(input())
n_1 = int(input())
res = a_1 * 100 * n_1 + b_1 * n_1
print(str(res) + " " + str((a_1 * 100 * n_1 + b_1 * n_1) % 100))