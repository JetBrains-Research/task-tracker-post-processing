# Copyright (c) 2017 Kelly Rivers
# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

from src.main.canonicalization.consts import TREE_TYPE
from src.main.util.log_util import log_and_raise_error
from src.main.canonicalization.transformations import *
from src.main.canonicalization.display import printFunction
from src.main.canonicalization.preprocessing_tree import runGiveIds
from src.main.canonicalization.ast_tools import getAllImports, getAllImportStatements

log = logging.getLogger(consts.LOGGER_NAME)


def get_ast(source: str) -> ast.AST:
    try:
        return ast.parse(source)
    except Exception as e:
        log.error(e)


def are_asts_equal(ast_1: ast.AST, ast_2: ast.AST) -> bool:
    return compareASTs(ast_1, ast_2) == 0


# Get code without extra spaces, comments and others (by calling printFunction from Kelly Rivers code)
def get_cleaned_code(source: str) -> str:
    return printFunction(get_ast(source))


def get_code_from_tree(tree: Optional[ast.AST]) -> str:
    return printFunction(tree)


# It is the transformations from Kelly Rivers code
def __get_canonical_transformations() -> List[Callable]:
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


def get_given_names(tree: ast.AST) -> List[str]:
    return [str(x) for x in getAllImports(tree)]


def get_imports(tree: ast.AST) -> List[str]:
    return getAllImportStatements(tree)


def __get_orig_tree_from_source(source: str) -> ast.AST:
    tree = get_ast(get_cleaned_code(source).rstrip('\n'))
    arg_types = get_arg_types()
    tree = propogateMetadata(tree, arg_types, {}, [0])
    orig_tree = deepcopy(tree)
    runGiveIds(orig_tree)
    return orig_tree


def __get_anon_tree_from_orig_tree(orig_tree: ast.AST, imports: List[str], to_simplify: bool = True) -> ast.AST:
    given_names = get_given_names(orig_tree)
    anon_tree = deepcopy(orig_tree)
    anon_tree = anonymizeNames(anon_tree, given_names, imports)
    if to_simplify:
        anon_tree = simplify(anon_tree)
    return anon_tree


def __get_canon_tree_from_anon_tree(anon_tree: ast.AST, imports: List[str]) -> ast.AST:
    transformations = __get_canonical_transformations()
    canon_tree = deepcopy(anon_tree)
    old_tree = None
    while compareASTs(old_tree, canon_tree, checkEquality=True) != 0:
        old_tree = deepcopy(canon_tree)

        helperFolding(canon_tree, None, imports)
        for t in transformations:
            canon_tree = t(canon_tree)
    return canon_tree


# Checks if the new tree has type that we want to get
# Returns updated gotten_trees
def __update_gotten_trees(new_tree: ast.AST, new_tree_type: TREE_TYPE, gotten_trees: Tuple[ast.AST, ...],
                          tree_types_to_get: Set[TREE_TYPE]) -> Tuple[ast.AST, ...]:
    if new_tree_type in tree_types_to_get:
        gotten_trees += (new_tree,)
        tree_types_to_get.remove(new_tree_type)
    return gotten_trees


# Use it to get orig_tree, anon_tree, canon_tree, or any combination of them by passing their types as tree_types_to_get
# It stops after getting all needed trees
def get_trees(source: str, tree_types_to_get: Set[TREE_TYPE], to_simplify: bool = True) -> Tuple[ast.AST, ...]:
    gotten_trees = ()
    # We shouldn't start getting trees if there is no tree types to get
    if not tree_types_to_get:
        return gotten_trees

    orig_tree = __get_orig_tree_from_source(source)

    # After getting the first tree (orig tree), we should check if we need to continue getting trees
    gotten_trees = __update_gotten_trees(orig_tree, TREE_TYPE.ORIG, gotten_trees, tree_types_to_get)
    if not bool(tree_types_to_get):
        return gotten_trees

    imports = get_imports(orig_tree)
    anon_tree = __get_anon_tree_from_orig_tree(orig_tree, imports, to_simplify=to_simplify)

    # After getting the second tree (anon tree), we should check if we need to continue getting trees
    gotten_trees = __update_gotten_trees(anon_tree, TREE_TYPE.ANON, gotten_trees, tree_types_to_get)
    if not bool(tree_types_to_get):
        return gotten_trees

    canon_tree = __get_canon_tree_from_anon_tree(anon_tree, imports)

    # After getting the third tree (canon tree), we should raise an error if there are still tree types to get
    gotten_trees = __update_gotten_trees(canon_tree, TREE_TYPE.CANON, gotten_trees, tree_types_to_get)
    if not bool(tree_types_to_get):
        return gotten_trees
    else:
        log_and_raise_error(f'There are still tree types to get {tree_types_to_get}, but trees getting is finished', log)
