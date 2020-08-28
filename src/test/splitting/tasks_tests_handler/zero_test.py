# Copyright (c) by anonymous author(s)

from typing import Callable, Tuple, Dict

import pytest

from src.test.test_config import to_skip, TEST_LEVEL
from src.main.util.consts import LANGUAGE, TASK
from src.test.splitting.tasks_tests_handler.util import run_test_task, SOLUTION

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


@pytest.mark.skipif(to_skip(current_module_level=TEST_LEVEL.SPLITTING), reason=TEST_LEVEL.SPLITTING.value)
class TestZeroTests:
    task = TASK.ZERO

    @staticmethod
    @pytest.fixture(scope="function",
                    params=[
                        (python_actual_pairs, LANGUAGE.PYTHON),
                        (java_actual_pairs, LANGUAGE.JAVA),
                        # (kotlin_actual_pairs, LANGUAGE.KOTLIN),
                        (cpp_actual_pairs, LANGUAGE.CPP)
                    ],
                    ids=[
                        'test_python',
                        'test_java',
                        # 'test_kotlin',
                        'test_cpp'
                    ]
                    )
    def param_language_test(request) -> Tuple[Dict[SOLUTION, Tuple[int, int]], LANGUAGE]:
        return request.param

    def test_language(self, param_language_test: Callable):
        actual_pairs, language = param_language_test
        run_test_task(self.task, actual_pairs, language)
