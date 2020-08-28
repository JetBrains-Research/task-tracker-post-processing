# Copyright (c) by anonymous author(s)

import pytest
import pandas as pd

from src.main.util import consts
from src.test.test_config import to_skip, TEST_LEVEL
from src.main.preprocessing.intermediate_diffs_removing import remove_intermediate_diffs_from_df

# Hidden SettingWithCopyWarning
pd.options.mode.chained_assignment = None

FRAGMENT = consts.CODE_TRACKER_COLUMN.FRAGMENT.value

source_1 = 'g3 = int(input())\nprint((g3 // 1))'
source_2 = 'g3 = int(input())\nprint((g3 // 10))'
source_3 = 'g3 = int(input())\nprint((g3 // 100))'
source_4 = 'g3 = int(input())\nprint((g2 // 100))'
source_5 = 'g2 = int(input())\nprint((g2 // 100))'

source_6 = 'print("hello")\nprint("world")'
source_7 = 'print("hello world")\nprint("world")'
source_8 = 'print("hello world")\nprint("hello world")'

source_9 = 'a=5\nb=9'
source_10 = 'a=50\nb=9\n'
source_11 = 'a=505\nb=900\n'
source_12 = 'a=505\nb=900\nprint()'


def run_removing_intermediate_diffs_test(input_df: pd.DataFrame, expected_df: pd.DataFrame) -> bool:
    input_df = remove_intermediate_diffs_from_df(input_df)
    input_df.index = [*range(input_df.shape[0])]
    return input_df.equals(expected_df)


@pytest.mark.skipif(to_skip(current_module_level=TEST_LEVEL.PREPROCESSING), reason=TEST_LEVEL.PREPROCESSING.value)
class TestRemoveIntermediateSteps:

    def test_no_diffs(self) -> None:

        #                               fragment
        # 0  g3 = int(input())\nprint((g3 // 1))
        # 1  g3 = int(input())\nprint((g3 // 1))
        # 2  g3 = int(input())\nprint((g3 // 1))
        # 3  g3 = int(input())\nprint((g3 // 1))
        # 4  g3 = int(input())\nprint((g3 // 1))
        input_df = pd.DataFrame({
            FRAGMENT: [source_1 for _ in range(5)]
        })

        #                               fragment
        # 0  g3 = int(input())\nprint((g3 // 1))
        # 1  g3 = int(input())\nprint((g3 // 1))
        # 2  g3 = int(input())\nprint((g3 // 1))
        # 3  g3 = int(input())\nprint((g3 // 1))
        # 4  g3 = int(input())\nprint((g3 // 1))
        expected_df = pd.DataFrame({
            FRAGMENT: [source_1 for _ in range(5)]
        })

        assert run_removing_intermediate_diffs_test(input_df, expected_df)

    def test_all_diffs_in_one_line(self) -> None:

        #                                 fragment
        # 0    g3 = int(input())\nprint((g3 // 1))
        # 1   g3 = int(input())\nprint((g3 // 10))
        # 2  g3 = int(input())\nprint((g3 // 100))
        # 3  g3 = int(input())\nprint((g2 // 100))
        # 4  g2 = int(input())\nprint((g2 // 100))
        input_df = pd.DataFrame({
            FRAGMENT: [source_1, source_2, source_3, source_4, source_5]
        })

        #                                 fragment
        # 0  g3 = int(input())\nprint((g2 // 100))
        # 1  g2 = int(input())\nprint((g2 // 100))
        expected_df = pd.DataFrame({
            FRAGMENT: [source_4, source_5]
        })

        assert run_removing_intermediate_diffs_test(input_df, expected_df)

    def test_next_and_after_next_lines(self) -> None:

        #                                      fragment
        # 0              print("hello")\nprint("world")
        # 1        print("hello world")\nprint("world")
        # 2  print("hello world")\nprint("hello world")
        input_df = pd.DataFrame({
            FRAGMENT: [source_6, source_7, source_8]
        })

        #                                      fragment
        # 0        print("hello world")\nprint("world")
        # 1  print("hello world")\nprint("hello world")
        expected_df = pd.DataFrame({
            FRAGMENT: [source_7, source_8]
        })

        assert run_removing_intermediate_diffs_test(input_df, expected_df)

    def test_diffs_in_different_lines(self) -> None:
        #                 fragment
        # 0               a=5\nb=9
        # 1            a=50\nb=9\n
        # 2         a=505\nb=900\n
        # 3  a=505\nb=900\nprint()
        input_df = pd.DataFrame({
            FRAGMENT: [source_9, source_10, source_11, source_12]
        })

        #                 fragment
        # 0            a=50\nb=9\n
        # 1         a=505\nb=900\n
        # 2  a=505\nb=900\nprint()
        expected_df = pd.DataFrame({
            FRAGMENT: [source_10, source_11, source_12]
        })

        assert run_removing_intermediate_diffs_test(input_df, expected_df)

    def test_first_line_is_none(self) -> None:
        #                 fragment
        # 0                    NaN
        # 1            a=50\nb=9\n
        # 2  a=505\nb=900\nprint()
        input_df = pd.DataFrame({
            FRAGMENT: [consts.DEFAULT_VALUE.FRAGMENT.value, source_10, source_12]
        })

        #                 fragment
        # 0                    NaN
        # 1            a=50\nb=9\n
        # 2  a=505\nb=900\nprint()
        expected_df = pd.DataFrame({
            FRAGMENT: [consts.DEFAULT_VALUE.FRAGMENT.value, source_10, source_12]
        })

        assert run_removing_intermediate_diffs_test(input_df, expected_df)
