# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import ast
import logging
from src.main.ast.ast_tools import getAllImports, getAllImportStatements
from src.main.ast.preprocessing_tree import runGiveIds
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


def get_code_from_tree(tree: ast.AST):
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


def __init_arg_types(arg_types: dict):
    if not arg_types:
        arg_types = {}
    return arg_types


def __init_given_names(given_names: list, tree: ast.AST):
    if not given_names:
        given_names = [str(x) for x in getAllImports(tree)]
    return given_names


def __init_imports(imports: list, tree: ast.AST):
    if not imports:
        imports = getAllImportStatements(tree)
    return imports


def get_canonicalized_form(source: str, given_names=None, arg_types=None, imports=None):
    tree = get_ast(get_cleaned_code(source).rstrip('\n'))

    given_names = __init_given_names(given_names, tree)
    arg_types = __init_arg_types(arg_types)
    imports = __init_imports(imports, tree)
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
