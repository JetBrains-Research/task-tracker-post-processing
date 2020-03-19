# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import os


from enum import Enum

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

class VERTEX_TYPE(Enum):
    START = 'start'
    END = 'end'
    INTERMEDIATE = 'intermediate'


FOLDER_WITH_CODE_FILES = ROOT_DIR + '/../../resources/solution_space'
FOLDER_WITH_CODE_FILES_FOR_TESTS = ROOT_DIR + '/../../resources/solution_space_tests'
GRAPH_FOLDER_PREFIX = 'graph_'
FILE_PREFIX = 'code_'
