# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import os
import logging
import unittest

from src.main.util.language_util import get_language_by_extension
from src.main.splitting.tasks_tests_handler import create_in_and_out_dict, check_tasks, run_tests
from src.main.util.consts import LOGGER_FORMAT, LOGGER_TEST_FILE, TEST_DATA_PATH, FILE_SYSTEM_ITEM, TASK
from src.main.util.file_util import get_all_file_system_items, get_extension_from_file, get_content_from_file

PREVIOUS_ERRORS_TEST_DATA = os.path.join(TEST_DATA_PATH, 'splitting/tasks_tests_handler/previous_errors')


# just to be sure it won't raise any errors again
class TestPreviousErrors(unittest.TestCase):
    def setUp(self) -> None:
        logging.basicConfig(filename=LOGGER_TEST_FILE, format=LOGGER_FORMAT, level=logging.INFO)

    def test_fragments(self):
        fragment_files = get_all_file_system_items(PREVIOUS_ERRORS_TEST_DATA, (lambda name: 'fragment' in name),
                                                   FILE_SYSTEM_ITEM.FILE.value)
        tasks = [t.value for t in TASK]
        in_and_out_files_dict = create_in_and_out_dict(tasks)

        for file in fragment_files:
            language = get_language_by_extension(get_extension_from_file(file))
            check_tasks(tasks, get_content_from_file(file), in_and_out_files_dict, language, False)

    # need to test ati_327/Main_67885, put it in PREVIOUS_ERRORS_TEST_DATA before running
    def test_codetracker_data(self):
        run_tests(PREVIOUS_ERRORS_TEST_DATA)


