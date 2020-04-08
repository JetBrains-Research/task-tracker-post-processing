# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import os
from enum import Enum

from src.main.canonicalization.diffs.diff_handler import DiffHandler

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


class VERTEX_TYPE(Enum):
    START = 'start'
    END = 'end'
    INTERMEDIATE = 'intermediate'


FOLDER_WITH_CODE_FILES = ROOT_DIR + '/../../resources/solution_space'
FOLDER_WITH_CODE_FILES_FOR_TESTS = ROOT_DIR + '/../../resources/test_data/solution_space'
EMPTY_CODE_FILE = ROOT_DIR + '/../../resources/solution_space/empty_code.py'
GRAPH_FOLDER_PREFIX = 'graph_'
FILE_PREFIX = 'code_'

DIFFS_PERCENT_TO_GO_DIRECTLY = 0.2
DISTANCE_TO_GRAPH_THRESHOLD = 2

EMPTY_DIFF_HANDLER = DiffHandler(source_code='')
