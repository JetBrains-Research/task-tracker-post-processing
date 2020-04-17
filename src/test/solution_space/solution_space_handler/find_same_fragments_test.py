# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import ast
import pytest
import logging
import pandas as pd
from typing import List, Tuple, Callable

from src.test.util import does_skip, TEST_LEVEL
from src.main.canonicalization.consts import TREE_TYPE
from src.main.solution_space.data_classes import AtiItem
from src.main.canonicalization.canonicalization import get_trees, are_asts_equal
from src.main.util.consts import LOGGER_NAME, CODE_TRACKER_COLUMN, ACTIVITY_TRACKER_COLUMN, ACTIVITY_TRACKER_EVENTS
from src.main.solution_space.solution_space_handler import __find_same_fragments, __get_ati_data, __get_column_value

log = logging.getLogger(LOGGER_NAME)


SOURCE_1 = 'print(\'Hello\')'
SOURCE_2 = 'print(\'Hello\')\nprint(\'Hello\')'

COUNT_SOURCE_1 = 5
COUNT_SOURCE_2 = 7


def __get_timestamps() -> List[int]:
    return list(range(0, COUNT_SOURCE_1)) + list(range(20, 20 + COUNT_SOURCE_2))


def __get_ati_event_types() -> List[str]:
    return [ACTIVITY_TRACKER_EVENTS.ACTION.value] * (COUNT_SOURCE_1 + COUNT_SOURCE_2)


def __get_ati_action_events() -> List[str]:
    return [ACTIVITY_TRACKER_EVENTS.action_events()[0]] * (COUNT_SOURCE_1 + COUNT_SOURCE_2)


def __get_fragments() -> List[str]:
    return [SOURCE_1] * COUNT_SOURCE_1 + [SOURCE_2] * COUNT_SOURCE_2


# We have a dataset:
#     timestamp                        fragment  timestampAti eventData eventType
# 0           0                  print('Hello')             0    Action       Run
# 1           1                  print('Hello')             1    Action       Run
# 2           2                  print('Hello')             2    Action       Run
# 3           3                  print('Hello')             3    Action       Run
# 4           4                  print('Hello')             4    Action       Run
# 5          20  print('Hello')\nprint('Hello')            20    Action       Run
# 6          21  print('Hello')\nprint('Hello')            21    Action       Run
# 7          22  print('Hello')\nprint('Hello')            22    Action       Run
# 8          23  print('Hello')\nprint('Hello')            23    Action       Run
# 9          24  print('Hello')\nprint('Hello')            24    Action       Run
# 10         25  print('Hello')\nprint('Hello')            25    Action       Run
# 11         26  print('Hello')\nprint('Hello')            26    Action       Run
def create_solutions() -> pd.DataFrame:
    return pd.DataFrame({CODE_TRACKER_COLUMN.TIMESTAMP.value: __get_timestamps(),
                         CODE_TRACKER_COLUMN.FRAGMENT.value: __get_fragments(),
                         ACTIVITY_TRACKER_COLUMN.TIMESTAMP_ATI.value: __get_timestamps(),
                         ACTIVITY_TRACKER_COLUMN.EVENT_DATA.value: __get_ati_action_events(),
                         ACTIVITY_TRACKER_COLUMN.EVENT_TYPE.value: __get_ati_event_types()})


def get_expected_out(solutions: pd.DataFrame, start_index: int, end_index: int) -> Tuple[int, List[AtiItem], ast.AST]:
    ati_elements = []
    fragment = __get_column_value(solutions, start_index, CODE_TRACKER_COLUMN.FRAGMENT)
    canon_tree, = get_trees(fragment, {TREE_TYPE.CANON})
    for i in range(start_index, end_index):
        ati_elements.append(__get_ati_data(solutions, i))
    return end_index, ati_elements, canon_tree


def __are_equal_ati_items_lists(expected_ati_items: List[AtiItem], actual_ati_items: List[AtiItem]) -> bool:
    if len(expected_ati_items) != len(actual_ati_items):
        return False
    for expected_ati_item, actual_ati_item in zip(expected_ati_items, actual_ati_items):
        if not expected_ati_item.__eq__(actual_ati_item):
            return False
    return True


def are_equal(expected_out: Tuple[int, List[AtiItem], ast.AST],
              actual_out: Tuple[int, List[AtiItem], ast.AST]) -> bool:
    expected_index, expected_ati_items, expected_tree = expected_out
    actual_index, actual_ati_items, actual_tree = actual_out
    return expected_index == actual_index and \
           __are_equal_ati_items_lists(expected_ati_items, actual_ati_items) and \
           are_asts_equal(expected_tree, actual_tree)


def get_actual_out(solutions: pd.DataFrame, index: int) -> Tuple[int, List[AtiItem], ast.AST]:
    i, ati_elements, current_tree = __find_same_fragments(solutions, index)
    return i, ati_elements, current_tree


@pytest.mark.skipif(does_skip(current_module_level=TEST_LEVEL.SOLUTION_SPACE), reason=TEST_LEVEL.SOLUTION_SPACE.value)
class TestFindSomeFragments:

    @staticmethod
    @pytest.fixture(scope="function",
                    params=[
                        (0, COUNT_SOURCE_1),
                        (3, COUNT_SOURCE_1),
                        (COUNT_SOURCE_1, COUNT_SOURCE_1 + COUNT_SOURCE_2),
                        (COUNT_SOURCE_1 + COUNT_SOURCE_2 - 1, COUNT_SOURCE_1 + COUNT_SOURCE_2),
                    ],
                    ids=[
                        'test_first_index',
                        'test_middle_index',
                        'test_middle_index_with_other_fragment',
                        'test_last_index'
                    ])
    def param_find_some_fragments_test(request):
        return request.param

    def test_find_some_fragments(self, param_find_some_fragments_test: Callable) -> None:
        (index, end_index) = param_find_some_fragments_test
        solutions = create_solutions()
        actual_out = get_actual_out(solutions, index)
        expected_out = get_expected_out(solutions, index, end_index)
        assert are_equal(expected_out, actual_out)
