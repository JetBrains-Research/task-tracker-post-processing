# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import os
import logging
import unittest

from typing import List, Tuple
from src.main.solution_space.data_classes import Code
from src.main.util.language_util import get_extension_by_language
from src.main.solution_space.solution_graph import Vertex, SolutionGraph
from src.test.solution_space.solution_graph.util import create_code_from_source, get_two_vertices
from src.main.util.file_util import get_all_file_system_items, all_items_condition, remove_directory
from src.main.solution_space.consts import GRAPH_FOLDER_PREFIX, FOLDER_WITH_CODE_FILES_FOR_TESTS, FILE_PREFIX
from src.main.util.consts import LOGGER_TEST_FILE, LOGGER_FORMAT, TEST_RESULT, LOGGER_NAME, TASK, FILE_SYSTEM_ITEM, \
    LANGUAGE

log = logging.getLogger(LOGGER_NAME)


CURRENT_TASK = TASK.PIES
NOT_DEFAULT_GRAPH_PREFIX = 'test_graph_'
NOT_DEFAULT_FILE_PREFIX = 'test_code_'
SolutionGraph.folder_with_code_files = FOLDER_WITH_CODE_FILES_FOR_TESTS


def get_test_folder_path(task: TASK = CURRENT_TASK) -> str:
    return os.path.join(FOLDER_WITH_CODE_FILES_FOR_TESTS, task.value)


def get_full_paths(short_paths: List[str]) -> List[str]:
    test_folder_path = get_test_folder_path()
    return [os.path.join(test_folder_path, s_p) for s_p in short_paths]


def create_three_graphs() -> Tuple[SolutionGraph, SolutionGraph, SolutionGraph]:
    sg_0 = SolutionGraph(CURRENT_TASK)
    sg_1 = SolutionGraph(CURRENT_TASK, file_prefix=NOT_DEFAULT_FILE_PREFIX)
    sg_2 = SolutionGraph(CURRENT_TASK, graph_folder_prefix=NOT_DEFAULT_GRAPH_PREFIX,
                         file_prefix=NOT_DEFAULT_FILE_PREFIX)
    return sg_0, sg_1, sg_2


def get_actual_folders_names() -> List[str]:
    return get_all_file_system_items(get_test_folder_path(), all_items_condition, FILE_SYSTEM_ITEM.SUBDIR.value)


def get_actual_files_names(folder: str) -> List[str]:
    return get_all_file_system_items(os.path.join(get_test_folder_path(), folder), all_items_condition,
                                     FILE_SYSTEM_ITEM.FILE.value)


def get_file_name(graph_id: int, code_id: int, graph_prefix: str = GRAPH_FOLDER_PREFIX, file_prefix: str = FILE_PREFIX,
                  language: LANGUAGE = LANGUAGE.PYTHON) -> str:
    return os.path.join(graph_prefix + str(graph_id), graph_prefix + str(graph_id) + '_' + file_prefix + str(code_id)
                        + str(get_extension_by_language(language).value))


# Reset graph, vertex and code last ids to avoid different ids in one-by-one test running and running them all at once
def init_default_ids() -> None:
    SolutionGraph._last_id = 0
    Vertex._last_id = 0
    Code._last_id = 0


def delete_folder() -> None:
    remove_directory(get_test_folder_path())


class TestCodeToFile(unittest.TestCase):
    def setUp(self) -> None:
        logging.basicConfig(filename=LOGGER_TEST_FILE, format=LOGGER_FORMAT, level=logging.INFO)

    # Create three graphs and check all folders names which were created for each graph
    def test_folders_names(self):
        delete_folder()
        init_default_ids()
        sg_0, sg_1, sg_2 = create_three_graphs()
        expected_folders_names = get_full_paths([GRAPH_FOLDER_PREFIX + '0',
                                                 GRAPH_FOLDER_PREFIX + '1',
                                                 NOT_DEFAULT_GRAPH_PREFIX + '2'])
        self.assertCountEqual(expected_folders_names, get_actual_folders_names())

    def test_folder_structure_with_default_files_names(self):
        init_default_ids()
        sg_0, _, _ = create_three_graphs()
        vertices = get_two_vertices(sg_0)
        folder = GRAPH_FOLDER_PREFIX + str(sg_0.id)
        actual_files_names = get_actual_files_names(folder)

        expected_files_names = get_full_paths([get_file_name(sg_0.id, 0), get_file_name(sg_0.id, 1)])
        self.assertCountEqual(expected_files_names, actual_files_names)

    def test_folder_structure_with_not_default_files_names(self):
        init_default_ids()
        _, sg_1, _ = create_three_graphs()
        vertices = get_two_vertices(sg_1)
        folder = GRAPH_FOLDER_PREFIX + str(sg_1.id)
        actual_files_names = get_actual_files_names(folder)

        expected_files_names = get_full_paths([get_file_name(sg_1.id, 0, file_prefix=NOT_DEFAULT_FILE_PREFIX),
                                               get_file_name(sg_1.id, 1, file_prefix=NOT_DEFAULT_FILE_PREFIX)])
        self.assertCountEqual(expected_files_names, actual_files_names)

    def test_folder_structure_with_all_not_default_names(self):
        init_default_ids()
        _, _, sg_2 = create_three_graphs()
        vertices = get_two_vertices(sg_2)
        folder = os.path.join(get_test_folder_path(), NOT_DEFAULT_GRAPH_PREFIX + str(sg_2.id))
        actual_files_names = get_actual_files_names(folder)

        expected_files_names = get_full_paths([get_file_name(sg_2.id, 0, file_prefix=NOT_DEFAULT_FILE_PREFIX,
                                                             graph_prefix=NOT_DEFAULT_GRAPH_PREFIX),
                                               get_file_name(sg_2.id, 1, file_prefix=NOT_DEFAULT_FILE_PREFIX,
                                                             graph_prefix=NOT_DEFAULT_GRAPH_PREFIX)])
        self.assertCountEqual(expected_files_names, actual_files_names)