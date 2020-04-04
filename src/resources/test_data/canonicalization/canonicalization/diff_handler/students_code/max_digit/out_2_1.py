new_var_0 = str(input())
max = '0'
for new_var_1 in new_var_0:
    if new_var_1.isdigit():
        int(new_var_1)
        if (new_var_1 > max):
            max = new_var_1
print(max)