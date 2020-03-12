# Copyright (c) 2017 Kelly Rivers
# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import ast
import logging

from src.main.util import consts
from src.main.canonicalization.transformations import *
from src.main.canonicalization.display import printFunction
from src.main.canonicalization.ast_tools import getAllImports, getAllImportStatements


log = logging.getLogger(consts.LOGGER_NAME)


def get_ast(source: str) -> ast.AST:
    try:
        return ast.parse(source)
    except Exception as e:
        log.error(e)


# Get code without extra spaces, comments and others (to call printFunction from Kelly Rivers code)
def get_cleaned_code(source: str) -> str:
    return printFunction(get_ast(source))


def get_code_from_tree(tree: ast.AST) -> str:
    return printFunction(tree)


# Return a new tree with anonymous names
def anonymize_names(tree: ast.AST) -> ast.AST:
    anon_tree = anonymizeNames(tree, get_given_names(tree), get_imports(tree))
    return anon_tree


# It is the transformations from Kelly Rivers code
def __get_canonical_transformations() -> list:
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


def get_arg_types() -> dict:
    return {}


def get_given_names(tree: ast.AST) -> list:
    return [str(x) for x in getAllImports(tree)]


def get_imports(tree: ast.AST) -> list:
    return getAllImportStatements(tree)


def get_canonicalized_form(source: str, given_names=None, arg_types=None, imports=None) -> ast.AST:
    tree = get_ast(get_cleaned_code(source).rstrip('\n'))

    if not given_names:
        given_names = get_given_names(tree)
    if not arg_types:
        arg_types = get_arg_types()
    if not imports:
        imports = get_imports(tree)

    transformations = __get_canonical_transformations()

    # tree preprocessing from Kelly Rivers code
    tree = propogateMetadata(tree, arg_types, {}, [0])
    tree = simplify(tree)
    tree = anonymizeNames(tree, given_names, imports)
    # Todo: correct handler for global ID
    # runGiveIds(tree)

    old_tree = None
    while compareASTs(old_tree, tree, checkEquality=True) != 0:
        old_tree = deepcopy(tree)
        helperFolding(tree, None, imports)
        for t in transformations:
            tree = t(tree)
    return tree
