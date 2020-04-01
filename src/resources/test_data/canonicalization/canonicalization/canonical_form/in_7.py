# Replace not (a > 4 and b > 5) to ((a <= 4) or (b <= 5)) and rename it
a = int(input())
b = int(input())
if not (a > 4 and b > 5):
    print("OK")
else:
    print("NOT OK")
