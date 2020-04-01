# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import pandas as pd

from src.test.test_util import LoggedTest
from src.main.preprocessing.code_tracker_handler import fill_column
from src.main.util.consts import CODE_TRACKER_COLUMN, DEFAULT_VALUE, INVALID_FILE_FOR_PREPROCESSING

INVALID_DF = pd.DataFrame({CODE_TRACKER_COLUMN.AGE.value: [11.0, 11.0, 11.0, 12.0]})

INVALID_DF_WITH_DEFAULT = pd.DataFrame({CODE_TRACKER_COLUMN.AGE.value: [11.0, 11.0, 11.0, 12.0,
                                                                        DEFAULT_VALUE.AGE.value,
                                                                        DEFAULT_VALUE.AGE.value]})

INVALID_DF_WITH_NONE = pd.DataFrame({CODE_TRACKER_COLUMN.AGE.value: [11.0, 11.0, None, 11.0, 12.0,  None]})

INVALID_DF_WITH_NONE_AND_DEFAULT = pd.DataFrame({CODE_TRACKER_COLUMN.AGE.value: [11.0, 11.0, None, 11.0,
                                     DEFAULT_VALUE.AGE.value, None, DEFAULT_VALUE.AGE.value]})

# It counts as containing only nan variables, so it becomes valid
INVALID_DF_WITHOUT_DATA = pd.DataFrame({CODE_TRACKER_COLUMN.AGE.value: [DEFAULT_VALUE.AGE.value, None, None,
                                                                        DEFAULT_VALUE.AGE.value]})

INVALID_DF_WITHOUT_RESTRICTION = pd.DataFrame({CODE_TRACKER_COLUMN.AGE.value: ["Fifteen"]})

INVALID_DFS = [INVALID_DF, INVALID_DF_WITH_DEFAULT, INVALID_DF_WITH_NONE, INVALID_DF_WITH_NONE_AND_DEFAULT,
               INVALID_DF_WITHOUT_RESTRICTION]

VALID_DF = pd.DataFrame({CODE_TRACKER_COLUMN.AGE.value: [11.0, 11.0, 11.0]})

VALID_DF_WITH_DEFAULT = pd.DataFrame({CODE_TRACKER_COLUMN.AGE.value: [11.0, 11.0, 11.0, DEFAULT_VALUE.AGE.value]})

VALID_DFS = [VALID_DF, VALID_DF_WITH_DEFAULT]

VALID_DF_ALL_DEFAULT = pd.DataFrame({CODE_TRACKER_COLUMN.AGE.value: [DEFAULT_VALUE.AGE.value, DEFAULT_VALUE.AGE.value,
                                                                     DEFAULT_VALUE.AGE.value]})

VALID_EMPTY_DF = pd.DataFrame({CODE_TRACKER_COLUMN.AGE.value: []})

DEFAULT_DFS = [VALID_DF_ALL_DEFAULT, VALID_EMPTY_DF]


class TestAGEColumnFilling(LoggedTest):

    def test_invalid_dfs(self) -> None:
        for invalid_df in INVALID_DFS:
            column_value = fill_column(invalid_df, CODE_TRACKER_COLUMN.AGE,
                                       CODE_TRACKER_COLUMN.AGE.fits_restrictions, DEFAULT_VALUE.AGE)
            self.assertEqual(INVALID_FILE_FOR_PREPROCESSING, column_value)

    def test_valid_dfs(self) -> None:
        for valid_df in VALID_DFS:
            column_value = fill_column(valid_df, CODE_TRACKER_COLUMN.AGE,
                                       CODE_TRACKER_COLUMN.AGE.fits_restrictions, DEFAULT_VALUE.AGE)
            self.assertEqual(11.0, column_value)

    def test_default_dfs(self) -> None:
        for default_df in DEFAULT_DFS:
            column_value = fill_column(default_df, CODE_TRACKER_COLUMN.AGE,
                                       CODE_TRACKER_COLUMN.AGE.fits_restrictions, DEFAULT_VALUE.AGE)
            self.assertTrue(DEFAULT_VALUE.AGE.is_equal(column_value))
