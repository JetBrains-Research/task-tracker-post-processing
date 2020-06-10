from typing import List, Tuple

import pytest

from src.test.test_config import to_skip, TEST_LEVEL
from src.main.canonicalization.canonicalization import get_ast
from src.main.canonicalization.ast_tools import AstStructure, ast


def get_sources_with_structure() -> List[Tuple[str, AstStructure]]:
    empty_structure = dict.fromkeys(AstStructure._nodes_to_count, 0)
    source_1 = 'a = 5\nif a > 4:\n    print(a)'
    structure_1 = empty_structure.copy()
    structure_1[ast.If] = 1
    structure_1 = AstStructure(structure_1)

    source_2 = 'a = 8\nwhile a > 4:\n    if a < 3:\n        print(a)\n    a -= 1'
    structure_2 = empty_structure.copy()
    structure_2[ast.If] = 1
    structure_2[ast.While] = 1
    structure_2 = AstStructure(structure_2)

    source_3 = 'a = 3'
    structure_3 = empty_structure.copy()
    structure_3 = AstStructure(structure_3)

    source_4 = 'a = 8\nfor i in range(a):\n    if i == 3:\n        print(i)\n    else:\n        print(i)'
    structure_4 = empty_structure.copy()
    structure_4[ast.For] = 1
    structure_4[ast.If] = 1
    structure_4 = AstStructure(structure_4)

    return [(source_1, structure_1), (source_2, structure_2), (source_3, structure_3), (source_4, structure_4)]


def get_sources_with_equal_structure() -> List[Tuple[str, str]]:
    source_1 = 'a = 9'
    source_2 = 'print(\'Hello!\')'

    source_3 = 'i = 0\nwhile i < 10:\n    print(i)\n    i += 1'
    source_4 = 'a = input()\nwhile a:\n    a = input()'

    source_5 = 'for i in range(8):\n    for j in range(8):\n        print(i * j)'
    source_6 = 'l = []\nfor i in range(23):\n    l.append(i)\nfor i in l:\n    print(i)'

    return [(source_1, source_2), (source_3, source_4), (source_5, source_6)]

def get_sources_for_subtraction() -> List[Tuple[str, str, int]]:
    source_1 = 'a = 4'
    source_2 = 'while True:\n    for i in range(10):\n        if i > 5:\n            print(i)'
    source_3 = 'if True:\n    print(\'True\')'

    return [(source_1, source_2, 3), (source_1, source_3, 1), (source_2, source_3, 2)]


@pytest.mark.skipif(to_skip(current_module_level=TEST_LEVEL.CANONICALIZATION),
                    reason=TEST_LEVEL.CANONICALIZATION.value)
class TestAstStructure:

    @pytest.mark.parametrize('source_with_structure', get_sources_with_structure())
    def test_getting_ast_structure(self, source_with_structure: Tuple[str, AstStructure]) -> None:
        source, expected_structure = source_with_structure
        actual_structure = AstStructure.get_ast_structure(get_ast(source))
        assert actual_structure.eq_counted_nodes(expected_structure)

    @pytest.mark.parametrize('equal_structure_sources', get_sources_with_equal_structure())
    def test_same_structures(self, equal_structure_sources: Tuple[str, str]) -> None:
        source_1, source_2 = equal_structure_sources
        structure_1 = AstStructure.get_ast_structure(get_ast(source_1))
        structure_2 = AstStructure.get_ast_structure(get_ast(source_2))
        assert structure_1.eq_counted_nodes(structure_2)

    @pytest.mark.parametrize('sources_for_subtraction', get_sources_for_subtraction())
    def test_sub_structures(self, sources_for_subtraction: Tuple[str, str, int]) -> None:
        source_1, source_2, expected_sub_res = sources_for_subtraction
        structure_1 = AstStructure.get_ast_structure(get_ast(source_1))
        structure_2 = AstStructure.get_ast_structure(get_ast(source_2))
        assert structure_1 - structure_2 == expected_sub_res == structure_2 - structure_1
