# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import logging
import unittest

from src.main.util import consts
from src.main.util.consts import LANGUAGE, TASK, LOGGER_FORMAT
from src.test.splitting.tasks_tests_handler.util import test_task, SOLUTION

python_actual_pairs = {
    SOLUTION.FULL.value: (8, 8),
    SOLUTION.PARTIAL.value: (8, 4),
    SOLUTION.WRONG.value: (8, 0),
    SOLUTION.ERROR.value: (-1, 1)
}

java_actual_pairs = {
    SOLUTION.FULL.value: (8, 8),
    SOLUTION.PARTIAL.value: (8, 4),
    SOLUTION.WRONG.value: (8, 0),
    SOLUTION.ERROR.value: (-1, 1)
}

kotlin_actual_pairs = {
    SOLUTION.FULL.value: (8, 8),
    SOLUTION.PARTIAL.value: (8, 4),
    SOLUTION.WRONG.value: (8, 0),
    SOLUTION.ERROR.value: (-1, 1)
}

cpp_actual_pairs = {
    SOLUTION.FULL.value: (8, 8),
    SOLUTION.PARTIAL.value: (8, 4),
    SOLUTION.WRONG.value: (8, 0),
    SOLUTION.ERROR.value: (-1, 1)
}


class TestZeroTests(unittest.TestCase):
    task = TASK.ZERO.value

    def setUp(self) -> None:
        logging.basicConfig(filename=consts.LOGGER_TEST_FILE, format=LOGGER_FORMAT, level=logging.INFO)

    def test_python(self):
        test_task(self, python_actual_pairs, LANGUAGE.PYTHON.value)

    def test_java(self):
        test_task(self, java_actual_pairs, LANGUAGE.JAVA.value)

    def test_kotlin(self):
        test_task(self, kotlin_actual_pairs, LANGUAGE.KOTLIN.value)

    def test_cpp(self):
        test_task(self, cpp_actual_pairs, LANGUAGE.CPP.value)
