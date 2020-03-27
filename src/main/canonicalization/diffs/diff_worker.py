# Copyright (c) 2017 Kelly Rivers
# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

from src.main.canonicalization.diffs.individualize import mapEdit
from src.main.canonicalization.diffs.generate_next_states import updateChangeVectors
from src.main.canonicalization.canonicalization import get_canonicalized_and_orig_form
from src.main.canonicalization.diffs.diff_asts import distance, diffAsts, printFunction


source_1 = 'a = int(input())\nb = int(input())\nn = int(input())\nres = (a * 100 * n + b * n)\nmy(str(res) + " " + str((a * 100 * n + b * n) % 100))'
source_2 = 'a = int(input())\nb = int(input())\nn = int(input())\nres = (a * 100 * n + b * n) // 100\nmy(str(res) + " " + str((a * 100 * n + b * n) % 100))'

print("SOURCE 1")
print(source_1)
print("______")
print("SOURCE 2")
print(source_2)
print("______")

tree_1, orig_tree_1 = get_canonicalized_and_orig_form(source_1)
tree_2, orig_tree_2 = get_canonicalized_and_orig_form(source_2)

dist, changes = distance(tree_1, tree_2)

print(dist, len(changes))

edit = diffAsts(tree_1, tree_2)
edit, _ = updateChangeVectors(edit, tree_1, tree_1)

print(changes)
print(edit)

edit = mapEdit(tree_1, orig_tree_1, edit)

print(edit)

for e in edit:
    e.start = orig_tree_1
    orig_tree_1 = e.applyChange()

print("RESULT")
print(printFunction(orig_tree_1))