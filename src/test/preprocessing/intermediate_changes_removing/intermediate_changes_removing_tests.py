# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import pandas as pd

from src.main.util import consts
from src.test.test_util import LoggedTest
from src.main.preprocessing.intermediate_changes_removing import __remove_intermediate_changes_from_df

FRAGMENT = consts.CODE_TRACKER_COLUMN.FRAGMENT.value

source_1 = 'g3 = int(input())\nprint((g3 // 1))'
source_2 = 'g3 = int(input())\nprint((g3 // 10))'
source_3 = 'g3 = int(input())\nprint((g3 // 100))'
source_4 = 'g3 = int(input())\nprint((g2 // 100))'
source_5 = 'g2 = int(input())\nprint((g2 // 100))'
source_6 = 'g2 = int(input())\nprint((g2 // 100))\nprint()'

source_7 = 'print("hello")\nprint("world")'
source_8 = 'print("hello world")\nprint("world")'
source_9 = 'print("hello world")\nprint("hello world")'


def run_test(input_df: pd.DataFrame, expected_df: pd.DataFrame) -> bool:
    input_df = __remove_intermediate_changes_from_df(input_df)
    input_df.index = [*range(input_df.shape[0])]
    return input_df.equals(expected_df)


class TestRemoveIntermediateSteps(LoggedTest):

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

        self.assertTrue(run_test(input_df, input_df))

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

        self.assertTrue(run_test(input_df, expected_df))

    def test_all_diffs_in_several_lines(self) -> None:

        #                                          fragment
        # 0             g3 = int(input())\nprint((g3 // 1))
        # 1           g3 = int(input())\nprint((g2 // 100))
        # 2           g2 = int(input())\nprint((g2 // 100))
        # 3  g2 = int(input())\nprint((g2 // 100))\nprint()
        input_df = pd.DataFrame({
            FRAGMENT: [source_1, source_4, source_5, source_6]
        })

        #                                          fragment
        # 0           g3 = int(input())\nprint((g2 // 100))
        # 1           g2 = int(input())\nprint((g2 // 100))
        # 2  g2 = int(input())\nprint((g2 // 100))\nprint()
        expected_df = pd.DataFrame({
            FRAGMENT: [source_4, source_5, source_6]
        })

        self.assertTrue(run_test(input_df, expected_df))

    def test_next_and_through_one_lines(self) -> None:

        #                                      fragment
        # 0              print("hello")\nprint("world")
        # 1        print("hello world")\nprint("world")
        # 2  print("hello world")\nprint("hello world")
        input_df = pd.DataFrame({
            FRAGMENT: [source_7, source_8, source_9]
        })

        #                                      fragment
        # 0        print("hello world")\nprint("world")
        # 1  print("hello world")\nprint("hello world")
        expected_df = pd.DataFrame({
            FRAGMENT: [source_8, source_9]
        })

        self.assertTrue(run_test(input_df, expected_df))
