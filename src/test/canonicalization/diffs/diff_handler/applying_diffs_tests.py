# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina
from src.test.canonicalization.diffs.diff_handler.diff_handler_tests import DST_FOLDER, apply_diffs
from src.test.canonicalization.util import run_test, DIFF_WORKER_TEST_TYPES
from src.test.test_util import LoggedTest


class TestApplyingDiffs(LoggedTest):

    # Find and apply all edits
    def test_diff_worker_with_all_edits(self) -> None:
        run_test(self, DIFF_WORKER_TEST_TYPES.DIFF_WORKER_TEST, apply_diffs,
                 additional_folder_name=DST_FOLDER,
                 to_clear_out=True)