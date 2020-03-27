# Copyright (c) 2017 Kelly Rivers
# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

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


# Get code without extra spaces, comments and others (to call printFunction from Kelly Rivers code)
def get_cleaned_code(source: str) -> str:
    return printFunction(get_ast(source))


def get_code_from_tree(tree: ast.AST) -> str:
    return printFunction(tree)


# Return a new tree with anonymous names
def get_anonymized_and_orig_tree(cleaned_tree: ast.AST, given_names: Optional[List[str]] = None,
                                 imports: Optional[List[str]] = None) -> Tuple[ast.AST, ast.AST]:
    orig_tree = deepcopy(cleaned_tree)
    runGiveIds(orig_tree)
    anon_tree = deepcopy(orig_tree)
    anon_tree = anonymizeNames(anon_tree, given_names, imports)
    return anon_tree, orig_tree


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


def get_canonicalized_and_orig_form(source: str, given_names: Optional[List[str]] = None,
                                    arg_types: Optional[dict] = None,
                                    imports: Optional[List[str]] = None) -> Tuple[ast.AST, ast.AST]:
    tree = get_ast(get_cleaned_code(source).rstrip('\n'))

    if not given_names:
        given_names = get_given_names(tree)
    if not arg_types:
        arg_types = get_arg_types()
    if not imports:
        imports = get_imports(tree)

    transformations = __get_canonical_transformations()

    # Tree preprocessing from Kelly Rivers code
    tree = propogateMetadata(tree, arg_types, {}, [0])
    tree, orig_tree = get_anonymized_and_orig_tree(tree, given_names, imports)
    tree = simplify(tree)
    # Todo: correct handler for global ID
    # runGiveIds(tree)

    old_tree = None
    while compareASTs(old_tree, tree, checkEquality=True) != 0:
        old_tree = deepcopy(tree)
        helperFolding(tree, None, imports)
        for t in transformations:
            tree = t(tree)
    return tree, orig_tree
