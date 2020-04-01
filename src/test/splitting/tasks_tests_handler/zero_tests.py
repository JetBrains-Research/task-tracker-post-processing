# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

from src.main.util.consts import LANGUAGE, TASK
from src.test.splitting.tasks_tests_handler.util import test_task, SOLUTION
from src.test.test_util import LoggedTest

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


class TestZeroTests(LoggedTest):
    task = TASK.ZERO

    def test_python(self) -> None:
        test_task(self, python_actual_pairs, LANGUAGE.PYTHON)

    def test_java(self) -> None:
        test_task(self, java_actual_pairs, LANGUAGE.JAVA)

    def test_kotlin(self) -> None:
        test_task(self, kotlin_actual_pairs, LANGUAGE.KOTLIN)

    def test_cpp(self) -> None:
        test_task(self, cpp_actual_pairs, LANGUAGE.CPP)
