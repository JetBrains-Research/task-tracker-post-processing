# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import pytest

from src.main.util.consts import TASK
from src.test.util import to_skip, TEST_LEVEL


CURRENT_TASK = TASK.PIES




@pytest.mark.skipif(to_skip(current_module_level=TEST_LEVEL.SOLUTION_SPACE), reason=TEST_LEVEL.SOLUTION_SPACE.value)
class TestGraphRepresentation:
    pass

