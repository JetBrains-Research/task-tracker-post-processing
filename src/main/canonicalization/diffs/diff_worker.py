# Copyright (c) 2017 Kelly Rivers
# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import ast
import logging

from typing import List
from src.main.util import consts
from src.main.canonicalization.diffs.individualize import mapEdit
from src.main.canonicalization.diffs.generate_next_states import updateChangeVectors
from src.main.canonicalization.canonicalization import get_canonicalized_and_orig_form
from src.main.canonicalization.diffs.diff_asts import distance, diffAsts, printFunction, ChangeVector


log = logging.getLogger(consts.LOGGER_NAME)


# source_1 = 'a = int(input())\nb = int(input())\nn = int(input())\nres = (a * 100 * n + b * n)\nprint(str(res) + " " + str((a * 100 * n + b * n) % 100))'
# source_2 = 'a = int(input())\nb = int(input())\nn = int(input())\nres = (a * 100 * n + b * n) // 100\nprint(str(res) + " " + str((a * 100 * n + b * n) % 100))'


def get_edits(source_tree: ast.AST, dest_tree: ast.AST) -> List[ChangeVector]:
    edits = diffAsts(source_tree, dest_tree)
    edits, _ = updateChangeVectors(edits, source_tree, source_tree)
    return edits


def apply_diffs(source_tree: ast.AST, source_orig_tree: ast.AST, edits: List[ChangeVector]) -> ast.AST:
    edits = mapEdit(source_tree, source_orig_tree, edits)
    for e in edits:
        e.start = source_orig_tree
        source_orig_tree = e.applyChange()
    return source_orig_tree


def main():
    source_1 = 'a = int(input())\nb = int(input())\nn = int(input())\nres = a * 100 + b * n\nprint(str(res) + " " + str((a * 100 * n + b * n) % 100))'
    source_2 = 'a = int(input())\nb = int(input())\nn = int(input())\nres = (a * 100 * n + b * n) // 100\nprint(str(res) + " " + str((a * 100 * n + b * n) % 100))'

    print("SOURCE 1")
    print(source_1)
    print("______")
    print("SOURCE 2")
    print(source_2)
    print("______")

    source_tree, source_orig_tree = get_canonicalized_and_orig_form(source_1)
    dest_source_tree, dest_source_orig_tree = get_canonicalized_and_orig_form(source_2)

    edits = get_edits(source_tree, dest_source_tree)

    orig_tree_1 = apply_diffs(source_tree, source_orig_tree, edits)

    print("RESULT")
    print(printFunction(source_orig_tree))


main()