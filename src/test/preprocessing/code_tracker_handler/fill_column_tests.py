import pandas as pd

from src.test.test_util import LoggedTest
from src.main.preprocessing.code_tracker_handler import fill_column
from src.main.util.consts import CODE_TRACKER_COLUMN, EXPERIENCE, DEFAULT_VALUE, INVALID_FILE_FOR_PREPROCESSING


INVALID_DF = pd.DataFrame({CODE_TRACKER_COLUMN.EXPERIENCE.value: [EXPERIENCE.FROM_FOUR_TO_SIX_YEARS.value,
                                                                  EXPERIENCE.FROM_FOUR_TO_SIX_YEARS.value,
                                                                  EXPERIENCE.FROM_FOUR_TO_SIX_YEARS.value,
                                                                  EXPERIENCE.FROM_HALF_TO_ONE_YEAR.value]})

INVALID_DF_WITH_DEFAULT = pd.DataFrame({CODE_TRACKER_COLUMN.EXPERIENCE.value: [EXPERIENCE.FROM_FOUR_TO_SIX_YEARS.value,
                                                                               EXPERIENCE.FROM_FOUR_TO_SIX_YEARS.value,
                                                                               EXPERIENCE.FROM_FOUR_TO_SIX_YEARS.value,
                                                                               EXPERIENCE.FROM_HALF_TO_ONE_YEAR.value,
                                                                               DEFAULT_VALUE.EXPERIENCE.value,
                                                                               DEFAULT_VALUE.EXPERIENCE.value]})

INVALID_WITH_NONE = pd.DataFrame({CODE_TRACKER_COLUMN.EXPERIENCE.value: [EXPERIENCE.FROM_FOUR_TO_SIX_YEARS.value,
                                                                         EXPERIENCE.FROM_FOUR_TO_SIX_YEARS.value,
                                                                         None,
                                                                         EXPERIENCE.FROM_FOUR_TO_SIX_YEARS.value,
                                                                         EXPERIENCE.FROM_HALF_TO_ONE_YEAR.value,
                                                                         None]})
# currently not included
INVALID_DF_WITH_NONE_AND_DEFAULT = pd.DataFrame(
    {CODE_TRACKER_COLUMN.EXPERIENCE.value: [EXPERIENCE.FROM_FOUR_TO_SIX_YEARS.value,
                                            EXPERIENCE.FROM_FOUR_TO_SIX_YEARS.value,
                                            None,
                                            EXPERIENCE.FROM_FOUR_TO_SIX_YEARS.value,
                                            DEFAULT_VALUE.EXPERIENCE.value,
                                            None,
                                            DEFAULT_VALUE.EXPERIENCE.value]})

INVALID_DFS = [INVALID_DF, INVALID_DF_WITH_DEFAULT, INVALID_WITH_NONE]


VALID_DF = pd.DataFrame({CODE_TRACKER_COLUMN.EXPERIENCE.value: [EXPERIENCE.FROM_FOUR_TO_SIX_YEARS.value,
                                                                EXPERIENCE.FROM_FOUR_TO_SIX_YEARS.value,
                                                                EXPERIENCE.FROM_FOUR_TO_SIX_YEARS.value]})

VALID_DF_WITH_DEFAULT = pd.DataFrame({CODE_TRACKER_COLUMN.EXPERIENCE.value: [EXPERIENCE.FROM_FOUR_TO_SIX_YEARS.value,
                                                                             EXPERIENCE.FROM_FOUR_TO_SIX_YEARS.value,
                                                                             EXPERIENCE.FROM_FOUR_TO_SIX_YEARS.value,
                                                                             DEFAULT_VALUE.EXPERIENCE.value]})

VALID_DFS = [VALID_DF, VALID_DF_WITH_DEFAULT]


VALID_DF_ALL_DEFAULT = pd.DataFrame({CODE_TRACKER_COLUMN.EXPERIENCE.value: [DEFAULT_VALUE.EXPERIENCE.value,
                                                                             DEFAULT_VALUE.EXPERIENCE.value,
                                                                             DEFAULT_VALUE.EXPERIENCE.value]})

VALID_EMPTY_DF = pd.DataFrame({CODE_TRACKER_COLUMN.EXPERIENCE.value: []})

DEFAULT_DFS = [VALID_DF_ALL_DEFAULT, VALID_EMPTY_DF]


class TestColumnFilling(LoggedTest):

    def test_invalid_dfs(self):
        for invalid_df in INVALID_DFS:
            column_value = fill_column(invalid_df, CODE_TRACKER_COLUMN.EXPERIENCE, DEFAULT_VALUE.EXPERIENCE)
            self.assertEqual(column_value, INVALID_FILE_FOR_PREPROCESSING)

    def test_valid_dfs(self):
        for valid_df in VALID_DFS:
            column_value = fill_column(valid_df, CODE_TRACKER_COLUMN.EXPERIENCE, DEFAULT_VALUE.EXPERIENCE)
            self.assertEqual(column_value, EXPERIENCE.FROM_FOUR_TO_SIX_YEARS.value)

    def test_default_dfs(self):
        for default_df in DEFAULT_DFS:
            column_value = fill_column(default_df, CODE_TRACKER_COLUMN.EXPERIENCE, DEFAULT_VALUE.EXPERIENCE)
            self.assertTrue(DEFAULT_VALUE.EXPERIENCE.is_equal(column_value))
