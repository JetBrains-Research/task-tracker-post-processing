import unittest

from main.splitting.tasks_tests_handler import check_python_file_by_mypy
from main.util.consts import TEST_DATA_PATH
from main.util.file_util import get_all_file_system_items

PARSING_TEST_DATA_PATH = TEST_DATA_PATH + "/tasks_tests_handler/python_parsing/"


class TestPythonParsing(unittest.TestCase):

    def test_all_python_errors(self):
        files = get_all_file_system_items(PARSING_TEST_DATA_PATH, (lambda _: True))
        for file in files:
            print(file)
            print(check_python_file_by_mypy(file))
                             # msg="Source code from " + get_file_name_from_path(file) + " should be incorrect")
