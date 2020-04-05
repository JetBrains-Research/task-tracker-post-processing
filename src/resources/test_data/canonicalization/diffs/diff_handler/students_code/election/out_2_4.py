dig_list = [int(input('enter 0 or 1: ')) for i in range(3)]
print(('1' if (sum(dig_list) > 1) else '0'))