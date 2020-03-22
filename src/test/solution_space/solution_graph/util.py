import ast

from src.main.solution_space.data_classes import Code
from src.main.util.consts import TEST_RESULT


def create_code_from_source(source: str, rate=TEST_RESULT.CORRECT_CODE.value) -> Code:
    return Code(ast.parse(source), rate)
