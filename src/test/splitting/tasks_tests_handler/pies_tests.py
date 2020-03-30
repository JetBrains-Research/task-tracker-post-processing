# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

from src.test.test_util import LoggedTest
from src.main.util.consts import LANGUAGE, TASK
from src.test.splitting.tasks_tests_handler.util import test_task, SOLUTION

python_actual_pairs = {
    SOLUTION.FULL.value: (8, 8),
    SOLUTION.PARTIAL.value: (8, 3),
    SOLUTION.WRONG.value: (8, 0),
    SOLUTION.ERROR.value: (-1, 1)
}

java_actual_pairs = {
    SOLUTION.FULL.value: (8, 8),
    SOLUTION.PARTIAL.value: (8, 3),
    SOLUTION.WRONG.value: (8, 0),
    SOLUTION.ERROR.value: (-1, 1)
}

kotlin_actual_pairs = {
    SOLUTION.FULL.value: (8, 8),
    SOLUTION.PARTIAL.value: (8, 3),
    SOLUTION.WRONG.value: (8, 0),
    SOLUTION.ERROR.value: (-1, 1)
}

cpp_actual_pairs = {
    SOLUTION.FULL.value: (8, 8),
    SOLUTION.PARTIAL.value: (8, 3),
    SOLUTION.WRONG.value: (8, 0),
    SOLUTION.ERROR.value: (-1, 1)
}


class TestPiesTests(LoggedTest):
    task = TASK.PIES

    def test_python(self):
        test_task(self, python_actual_pairs, LANGUAGE.PYTHON)

    def test_java(self):
        test_task(self, java_actual_pairs, LANGUAGE.JAVA)

    def test_kotlin(self):
        test_task(self, kotlin_actual_pairs, LANGUAGE.KOTLIN)

    def test_cpp(self):
        test_task(self, cpp_actual_pairs, LANGUAGE.CPP)
