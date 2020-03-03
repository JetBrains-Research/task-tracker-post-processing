# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import ast
import logging
from src.main.ast.ast_tools import getAllImports, getAllImportStatements
from src.main.ast.transformations import *
from src.main.util import consts
from src.main.ast.display import printFunction


log = logging.getLogger(consts.LOGGER_NAME)


def get_ast(source: str):
    try:
        return ast.parse(source)
    except Exception as e:
        log.error(e)


# Get code without extra spaces, comments and others (to call printFunction from Kelly Rivers code)
def get_cleaned_code(source: str):
    return printFunction(get_ast(source))


def print_tree(tree: ast.AST):
    return printFunction(tree)


# Return a new tree with anonymous names
def anonymize_names(tree: ast.AST):
    given_names = [str(x) for x in getAllImports(tree)]
    imports = getAllImportStatements(tree)
    anon_tree = anonymizeNames(tree, given_names, imports)
    return anon_tree


# It is the transformations from Kelly Rivers code
def __get_canonical_transformations():
    return [
                constantFolding,

                cleanupEquals,
                cleanupBoolOps,
                cleanupRanges,
                cleanupSlices,
                cleanupTypes,
                cleanupNegations,

                conditionalRedundancy,
                combineConditionals,
                collapseConditionals,

                copyPropagation,

                deMorganize,
                orderCommutativeOperations,

                deadCodeRemoval
                ]


def get_canonical_form(tree):
    transformations = __get_canonical_transformations()

    oldTree = None
    while compareASTs(oldTree, tree, checkEquality=True) != 0:
        oldTree = deepcopy(tree)
        for t in transformations:
            tree = t(tree)

    return tree


source = "n=int(input())\nA=[int(i)for i in input().split()]\nk=0\nA=sorted(A)\nwhile k>n and A[k]!=0 and A[k]<1:\n    k+=1\nif A[k]==0:\n    print('YES')\nelse:\n    print('NO')"


anon_tree = get_ast(get_cleaned_code(source).rstrip('\n'))
canonical_form = get_canonical_form(anon_tree)
print_tree(canonical_form)

