new_var_0 = int(input())
new_var_1 = int(input())
new_var_2 = int(input())
new_var_3 = []
new_var_4 = []
if (new_var_0 == 1):
    new_var_4.append(new_var_0)
else:
    new_var_3.append(new_var_0)
if (new_var_1 == 1):
    new_var_4.append(new_var_1)
else:
    new_var_3.append(new_var_1)
if (new_var_2 == 1):
    new_var_4.append(new_var_2)
else:
    new_var_3.append(new_var_2)
new_var_5 = len(new_var_3)
dig_list = len(new_var_4)
if (new_var_5 < dig_list):
    print(1)
elif (new_var_5 > dig_list):
    print(0)