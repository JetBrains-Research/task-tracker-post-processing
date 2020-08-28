# Copyright (c) by anonymous author(s)

import logging
from typing import List, Tuple, Callable

import pytest

from src.test.test_config import to_skip, TEST_LEVEL
from src.main.solution_space.serialized_code import Code
from src.main.util.consts import LOGGER_NAME, TEST_RESULT
from src.main.util.helper_classes.id_counter import IdCounter
from src.main.solution_space.data_classes import CodeInfo, User
from src.main.solution_space.solution_space_handler import __remove_loops


log = logging.getLogger(LOGGER_NAME)

user = User()
code_info = CodeInfo(user)

source_1 = ''
source_2 = 'a = int(input())'
source_3 = 'a = int(input())\nb = int(input())'
source_4 = 'a = int(input())\nb = int(input())\nc = int(input())'
source_5 = 'a = int(input())\nb = int(input())\nc = int(input())\nprint(a * c + " " + b * c)'

sources = [source_1, source_2, source_3, source_4, source_5]


def get_code_chain_from_sources(start_index: int = 0, end_index: int = len(sources)) -> List[Tuple[Code, CodeInfo]]:
    IdCounter.reset_all()
    return [(Code.from_source(source, TEST_RESULT.CORRECT_CODE.value), code_info)
            for source in sources[start_index: end_index]]


# [source_1, source_2, source_3, source_1, source_3]
def get_code_chain_with_one_loop() -> List[Tuple[Code, CodeInfo]]:
    return get_code_chain_from_sources(0, 3) + get_code_chain_from_sources(0, 1) + get_code_chain_from_sources(2, 3)


# [source_1, source_2, source_3, source_1]
def get_code_chain_with_same_start_and_end() -> List[Tuple[Code, CodeInfo]]:
    return get_code_chain_from_sources(0, 3) + get_code_chain_from_sources(0, 1)


# [source_1, source_2, source_3, source_4, source_5, source_3, source_1]
def get_code_chain_with_nested_loop() -> List[Tuple[Code, CodeInfo]]:
    return get_code_chain_from_sources(0, 4) + get_code_chain_from_sources(2, 3) + get_code_chain_from_sources(0, 1)


# [source_1, source_2, source_3, source_1, source_4, source_5, source_4]
def get_code_chain_with_several_loops() -> List[Tuple[Code, CodeInfo]]:
    return get_code_chain_from_sources(0, 3) + get_code_chain_from_sources(0, 1) + get_code_chain_from_sources(3, 5) \
           + get_code_chain_from_sources(3, 4)


# [source_1, source_1, source_1]
def get_code_chain_with_same_elements() -> List[Tuple[Code, CodeInfo]]:
    return get_code_chain_from_sources(0, 1) * 3


# [source_2, source_3, source_1, source_4]
def get_code_chain_with_empty_fragment() -> List[Tuple[Code, CodeInfo]]:
    return get_code_chain_from_sources(1, 3) + get_code_chain_from_sources(0, 1) + get_code_chain_from_sources(3, 4)


def get_chain_without_loops(chain: List[Tuple[Code, CodeInfo]]) -> List[Tuple[Code, CodeInfo]]:
    return __remove_loops(chain, user)


def compare_chains(chain_without_loops: List[Tuple[Code, CodeInfo]],
                   expected_chain: List[Tuple[Code, CodeInfo]]) -> bool:
    if len(chain_without_loops) != len(expected_chain):
        return False
    for first, second in zip(chain_without_loops, expected_chain):
        if first[0].get_pretty_string() != second[0].get_pretty_string():
            return False
    return True


@pytest.mark.skipif(to_skip(current_module_level=TEST_LEVEL.SOLUTION_SPACE), reason=TEST_LEVEL.SOLUTION_SPACE.value)
class TestRemoveLoops:

    @staticmethod
    @pytest.fixture(scope="function",
                    params=[
                        # [source_1, source_2, source_3, source_4] -> [source_1, source_2, source_3, source_4]
                        (get_code_chain_from_sources(0, 4), get_code_chain_from_sources(0, 4)),
                        # [source_1, source_2, source_3, source_1, source_3] -> [source_1, source_3]
                        (get_code_chain_with_one_loop(), get_code_chain_from_sources(0, 1) + get_code_chain_from_sources(2, 3)),
                        # [source_1, source_2, source_3, source_1] -> [source_1]
                        (get_code_chain_with_same_start_and_end(), get_code_chain_from_sources(0, 1)),
                        # [source_1, source_2, source_3, source_4, source_5, source_3, source_1] -> [source_1]
                        (get_code_chain_with_nested_loop(), get_code_chain_from_sources(0, 1)),
                        # [source_1, source_2, source_3, source_1, source_4, source_5, source_4] -> [source_1, source_4]
                        (get_code_chain_with_several_loops(), get_code_chain_from_sources(0, 1) + get_code_chain_from_sources(3, 4)),
                        # [source_1, source_1, source_1] -> [source_1]
                        (get_code_chain_with_same_elements(), get_code_chain_from_sources(0, 1)),
                        # [source_2, source_3, source_1, source_4] -> [source_1, source_4],
                        # because source_1 is empty fragment
                        (get_code_chain_with_empty_fragment(), get_code_chain_from_sources(0, 1) + get_code_chain_from_sources(3, 4)),
                    ],
                    ids=[
                        'test_code_chain_without_loops',
                        'test_code_chain_with_one_loop',
                        'test_code_chain_with_same_start_and_end',
                        'test_code_chain_with_nested_loop',
                        'test_code_chain_with_several_loops',
                        'test_code_chain_with_same_elements',
                        'test_code_chain_with_empty_fragment'
                    ])
    def param_remove_loops_test(request) -> Tuple[List[Tuple[Code, CodeInfo]], List[Tuple[Code, CodeInfo]]]:
        return request.param

    def test_remove_loops(self, param_remove_loops_test: Callable) -> None:
        (source_chain, expected_chain) = param_remove_loops_test
        assert compare_chains(get_chain_without_loops(source_chain), expected_chain)
