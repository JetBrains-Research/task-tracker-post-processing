# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

from typing import Tuple, Callable

import pytest
import pandas as pd

from src.test.util import to_skip, TEST_LEVEL
from src.main.util.consts import CODE_TRACKER_COLUMN
from src.main.util.data_util import crop_data_by_timestamp

END_INDEX = 100
COLUMN = CODE_TRACKER_COLUMN.TIMESTAMP


def get_source_data() -> pd.DataFrame:
    timestamps = range(0, END_INDEX)
    return pd.DataFrame({
            COLUMN.value: timestamps
        })


def get_data_with_deleted_by_start_and_end() -> Tuple[pd.DataFrame, int, int]:
    start = 5
    end = 10
    timestamps = range(start, end + 1)
    return pd.DataFrame({
        COLUMN.value: timestamps
    }), start, end


def get_data_with_deleted_by_start() -> Tuple[pd.DataFrame, int, None]:
    start = 5
    timestamps = range(start, END_INDEX)
    return pd.DataFrame({
        COLUMN.value: timestamps
    }), start, None


def are_equal(df_1: pd.DataFrame, df_2: pd.DataFrame) -> bool:
    df_1.index = [*range(df_1.shape[0])]
    df_2.index = [*range(df_2.shape[0])]
    return df_1.equals(df_2)


def run_test(get_data_for_test: Callable) -> bool:
    source_data = get_source_data()
    expected_crop_data, start, end = get_data_for_test()
    actual_data = crop_data_by_timestamp(source_data, COLUMN, start, end)
    return are_equal(actual_data, expected_crop_data)


@pytest.mark.skipif(to_skip(current_module_level=TEST_LEVEL.UTIL), reason=TEST_LEVEL.UTIL.value)
class TestDataUtilMethods:

    def test_crop_data_by_start_and_end(self) -> None:
        assert run_test(get_data_with_deleted_by_start_and_end)

    def test_crop_data_by_start(self) -> None:
        assert run_test(get_data_with_deleted_by_start)



