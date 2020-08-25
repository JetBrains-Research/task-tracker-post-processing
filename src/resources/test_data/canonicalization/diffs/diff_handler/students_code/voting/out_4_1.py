new_var_0 = int(input())
new_var_4 = int(input())
new_var_1 = int(input())
new_var_2 = []
new_var_3 = []
if (new_var_0 == 1):
    new_var_3.append(new_var_0)
else:
    new_var_2.append(new_var_0)
if (new_var_4 == 1):
    new_var_3.append(new_var_4)
else:
    new_var_2.append(new_var_4)
if (new_var_1 == 1):
    new_var_3.append(new_var_1)
else:
    new_var_2.append(new_var_1)
if (len(new_var_2) < len(new_var_3)):
    print(1)
elif (len(new_var_3) < len(new_var_2)):
    print(0)