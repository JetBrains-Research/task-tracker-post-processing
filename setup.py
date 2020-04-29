# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import sys
import argparse
from setuptools import setup, find_packages

import src
from src.test.test_config import get_level_by_param

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('requirements.txt') as req_file:
    install_requires = req_file.read()

# Todo: find a better way for it
# See: https://docs.pytest.org/en/latest/example/simple.html#pass-different-values-to-a-test-function-depending-on-command-line-options
args = sys.argv
test_level_param = '--test_level'

if test_level_param in args:
    parser = argparse.ArgumentParser()
    parser.add_argument('test', action='store', choices=['test'], help='Action type')
    parser.add_argument(test_level_param, action='store', dest='test_level_key', help='Test level key', type=str)
    args = parser.parse_args()
    src.test.test_config.CURRENT_TEST_LEVEL = get_level_by_param(args.test_level_key)
    sys.argv.remove(test_level_param)
    sys.argv.remove(args.test_level_key)

setup(name='codetracker-data',
      # version='1.0.0',
      description='Data preprocessing, hint generation algorithm',
      url='https://github.com/elena-lyulina/codetracker-data',
      author='Anastasiia Birillo, Elena Lyulina',
      long_description_content_type='text/markdown',
      long_description=readme,
      license='MIT',
      packages=find_packages(),
      python_requires='>=3'
      )
