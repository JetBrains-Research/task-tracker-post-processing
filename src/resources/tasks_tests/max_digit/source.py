a = int(input())
b = int(input())
c = int(input())
List = []
List1 = []
if a == 0 or b == 0 or c == 0:
    List.append(0)
elif a == 1 or b == 1 or c == 1:
    List1.append(1)
if len(List) > len(List1):
    print(0)
elif len(List) < len(List1):
    print(1)