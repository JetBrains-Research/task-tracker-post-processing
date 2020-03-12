# Replace not (a <= b) to (g0 < g1) and rename it
a = input()
b = input()
if not (a <= b):
    print("OK")
else:
    print("NOT OK")