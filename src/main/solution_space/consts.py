# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import os
from enum import Enum

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


class VERTEX_TYPE(Enum):
    START = 'start'
    END = 'end'
    INTERMEDIATE = 'intermediate'


SOLUTION_SPACE_FOLDER = ROOT_DIR + '/../../resources/solution_space'
TEST_SYSTEM_GRAPH = ROOT_DIR + '/../../resources/test_system/test_system_graph.pickle'
SOLUTION_SPACE_TEST_FOLDER = ROOT_DIR + '/../../resources/test_data/solution_space'
EMPTY_CODE_FILE = ROOT_DIR + '/../../resources/solution_space/empty_code.py'
GRAPH_FOLDER_PREFIX = 'graph'
FILE_PREFIX = 'code'

NODES_NUMBER_PERCENT_TO_GO_DIRECTLY = 0.2
DIFFS_PERCENT_TO_GO_DIRECTLY = 0.2
DISTANCE_TO_GRAPH_THRESHOLD = 2
ROLLBACK_PROBABILITY = 0.7

NODE_NUMBERS_RATE = 0.2
CANON_TOP_N = 5
ANON_TOP_N = 10


