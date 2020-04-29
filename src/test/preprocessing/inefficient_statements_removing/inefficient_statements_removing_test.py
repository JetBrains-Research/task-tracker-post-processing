# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import pytest
import pandas as pd

from src.main.util import consts
from src.test.test_config import to_skip, TEST_LEVEL
from src.main.preprocessing.inefficient_statements_removing import __remove_inefficient_statements_from_df

# Hidden SettingWithCopyWarning
pd.options.mode.chained_assignment = None

FRAGMENT = consts.CODE_TRACKER_COLUMN.FRAGMENT.value

source_1 = 'g3 = int(input())\nprint((g3 // 1))\nprint'
source_2 = 'g3 = int\nprint()'
source_3 = 'g3 = int\n0\nprint()'


def run_test(input_df: pd.DataFrame, expected_df: pd.DataFrame) -> bool:
    input_df = __remove_inefficient_statements_from_df(input_df)
    input_df.index = [*range(input_df.shape[0])]
    return input_df.equals(expected_df)


@pytest.mark.skipif(to_skip(current_module_level=TEST_LEVEL.PREPROCESSING), reason=TEST_LEVEL.PREPROCESSING.value)
class TestPylintChecker:

    def test_inefficient_statements(self) -> None:

        #                                      fragment
        # 0  g3 = int(input())\nprint((g3 // 1))\nprint
        # 1                           g3 = int\nprint()
        # 2                        g3 = int\n0\nprint()
        input_df = pd.DataFrame({
            FRAGMENT: [source_1, source_2, source_3]
        })

        #             fragment
        # 0  g3 = int\nprint()
        expected_df = pd.DataFrame({
            FRAGMENT: [source_2]
        })

        assert run_test(input_df, expected_df)
