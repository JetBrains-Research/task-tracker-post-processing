import os
import logging
import unittest

from src.main.util import consts
from src.main.util.file_util import get_all_file_system_items, change_extension_to

log = logging.getLogger(consts.LOGGER_NAME)


def get_module_from_file(file: str):
    file = os.path.abspath(file)
    return change_extension_to(file[file.index('src/test'):], '').replace('/', '.')


test_files = get_all_file_system_items(consts.TEST_PATH, (lambda f: f.endswith('_tests.py')),
                                       consts.FILE_SYSTEM_ITEM.FILE.value)
test_modules = list(map(get_module_from_file, test_files))

suite = unittest.TestSuite()

for t in test_modules:
    try:
        # If the module defines a suite() function, call it to get the suite
        mod = __import__(t, globals(), locals(), ['suite'])
        suite_fn = getattr(mod, 'suite')
        suite.addTest(suite_fn())
    except (ImportError, AttributeError):
        # Else, just load all the test cases from the module
        suite.addTest(unittest.defaultTestLoader.loadTestsFromName(t))

runner = unittest.TextTestRunner()
test_result = runner.run(suite)

log.debug('Finish testing modules ' + str(test_modules) + '. Errors count: ' + str(
    len(test_result.errors)) + '. Failures count: ' + str(len(test_result.failures)) + '. Skipped count: ' + str(
    len(test_result.skipped)) + '. Run count: ' + str(test_result.testsRun))
