# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import os

import pytest

from src.main.util.consts import TEST_DATA_PATH, TASK
from src.main.util.language_util import get_language_by_extension
from src.main.task_scoring.tasks_tests_handler import create_in_and_out_dict, check_tasks, run_tests
from src.main.util.file_util import get_all_file_system_items, get_extension_from_file, get_content_from_file

PREVIOUS_ERRORS_TEST_DATA = os.path.join(TEST_DATA_PATH, 'task_scoring/tasks_tests_handler/previous_errors')

REASON = 'These tests aren\'t included in all tests running because the stage of getting tasks rates has already ' \
         'passed. \nAll previous cases when some fragments had raised any errors while getting rates are fixed now.'


@pytest.mark.skip(reason=REASON)
# just to be sure it won't raise any errors again
class TestPreviousErrors:

    @pytest.mark.parametrize('fragment_file', get_all_file_system_items(PREVIOUS_ERRORS_TEST_DATA,
                                                                        (lambda name: 'fragment' in name)))
    def test_fragments(self, fragment_file: str) -> None:
        in_and_out_files_dict = create_in_and_out_dict(TASK.tasks())
        language = get_language_by_extension(get_extension_from_file(fragment_file))
        check_tasks(TASK.tasks(), get_content_from_file(fragment_file), in_and_out_files_dict, language, False)

    # need to test ati_327/Main_67885, put it in PREVIOUS_ERRORS_TEST_DATA before running
    def test_codetracker_data(self) -> None:
        run_tests(PREVIOUS_ERRORS_TEST_DATA)
