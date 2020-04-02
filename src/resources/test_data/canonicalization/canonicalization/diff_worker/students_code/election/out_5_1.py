new_var_0 = int(input())
new_var_1 = int(input())
new_var_3 = int(input())
new_var_2 = []
a = []
if (new_var_0 == 1):
    a.append(new_var_0)
else:
    new_var_2.append(new_var_0)
if (new_var_1 == 1):
    a.append(new_var_1)
else:
    new_var_2.append(new_var_1)
if (new_var_3 == 1):
    a.append(new_var_3)
else:
    new_var_2.append(new_var_3)
if (len(new_var_2) < len(a)):
    print(1)
elif (len(a) < len(new_var_2)):
    print(0)