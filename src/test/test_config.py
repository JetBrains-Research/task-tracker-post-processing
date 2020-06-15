# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

from enum import Enum


class TEST_LEVEL(Enum):
    # Run all tests in the project
    ALL = 'all tests'

    # Run only canonicalization tests
    CANONICALIZATION = 'canonicalization tests'

    # Run only solution space tests
    SOLUTION_SPACE = 'solution space tests'

    # Run only plots tests
    PLOTS = 'plots tests'

    # Run only preprocessing tests
    PREPROCESSING = 'preprocessing tests'

    # Run only splitting tests
    SPLITTING = 'splitting tests'

    # Run only util tests
    UTIL = 'util tests'

    # Run only cli tests
    CLI = 'cli tests'


CURRENT_TEST_LEVEL = TEST_LEVEL.ALL


def to_skip(current_module_level: TEST_LEVEL) -> bool:
    # If we want to run all tests, we don't want skip tests in the all modules
    if CURRENT_TEST_LEVEL == TEST_LEVEL.ALL:
        return False
    return current_module_level != CURRENT_TEST_LEVEL


PARAMS_AND_TEST_LEVEL_DICT = {
    'all': TEST_LEVEL.ALL,
    'canon': TEST_LEVEL.CANONICALIZATION,
    'solution_space': TEST_LEVEL.SOLUTION_SPACE,
    'plots': TEST_LEVEL.PLOTS,
    'preprocess': TEST_LEVEL.PREPROCESSING,
    'splitting': TEST_LEVEL.SPLITTING,
    'util': TEST_LEVEL.UTIL,
    'cli': TEST_LEVEL.CLI
}


def __get_available_levels_info():
    info = ''
    params = PARAMS_AND_TEST_LEVEL_DICT.keys()
    for param in params:
        info += f'{param} - {PARAMS_AND_TEST_LEVEL_DICT[param].value}\n'
    return info


def get_level_by_param(param: str) -> TEST_LEVEL:
    param = param.strip().lower()
    test_level = PARAMS_AND_TEST_LEVEL_DICT.get(param, None)
    if test_level is None:
        raise ValueError(f'Incorrect level for tests. Available levels:\n{__get_available_levels_info()}')
    return test_level


