# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import logging

from src.main.util import consts

log = logging.getLogger(consts.LOGGER_NAME)

'''
Use GumTreeDiff for getting diffs between ASTs and for applying it
Source code: https://github.com/GumTreeDiff/gumtree
'''


def get_diffs_number(source_file: str, destination_file: str) -> int:
    # Todo: implement it
    pass
    return 0


def apply_diffs(source_file: str, destination_file: str) -> str:
    pass
