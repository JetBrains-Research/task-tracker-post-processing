from src.main import consts
import unittest
import logging

log = logging.getLogger(consts.LOGGER_NAME)

test_modules = [
    'src.tests.activity_tracker_handler.time_methods',
    'src.tests.activity_tracker_handler.dataframe_methods'
]

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
