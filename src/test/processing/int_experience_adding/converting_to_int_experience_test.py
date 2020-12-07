from typing import Tuple, Any

import pytest

from src.test.test_config import to_skip, TEST_LEVEL
from src.main.util.consts import EXPERIENCE, INT_EXPERIENCE, DEFAULT_VALUE
from src.main.processing.int_experience_adding import convert_to_int_experience


# We expect that each EXPERIENCE value is converted to int; None and -1 (in case of INVALID_FILE_FOR_PREPROCESSING) are
# converted to DEFAULT_VALUE.INT_EXPERIENCE

experiences = EXPERIENCE.values() + [None, -1]
int_experiences = INT_EXPERIENCE.values() + [DEFAULT_VALUE.INT_EXPERIENCE.value, DEFAULT_VALUE.INT_EXPERIENCE.value]


@pytest.mark.skipif(to_skip(current_module_level=TEST_LEVEL.PROCESSING), reason=TEST_LEVEL.PROCESSING.value)
class TestConvertingToIntExperience:

    @pytest.mark.parametrize('index_experience', enumerate(experiences))
    def test_adding_int_experience(self, index_experience: Tuple[int, Any]) -> None:
        i, experience = index_experience
        int_experience = convert_to_int_experience(experience)
        assert int_experience == int_experiences[i]

