# codetracker-data

### Description

Todo: add description

---

### Run tests

We use [`pytest`](https://docs.pytest.org/en/latest/contents.html) library for tests.

__Note__: If you have `ModuleNotFoundError` while you try to run tests, please call `pip install -e .`
 before using the test system.

Use `python setup.py test` from the root directory to run __ALL__ tests. 
If you want to run a part of tests, please use `param --test_level`.

You can use different test levels for `param --test_level`:

Param | Description 
--- | --- 
__all__ | all tests from all modules (it is the default value)
__canon__ | tests from the canonicalization module
__solution_space__ | tests from the solution space module 
__plots__ | tests from the plots module 
__preprocess__ | tests from the preprocessing module 
__splitting__ | tests from the splitting module 
__util__ | tests from the util module 
