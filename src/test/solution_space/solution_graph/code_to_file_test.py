# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import os
import logging
import unittest
from typing import List, Tuple

import pytest

from src.test.util import to_skip, TEST_LEVEL
from src.main.solution_space.solution_graph import SolutionGraph
from src.main.util.language_util import get_extension_by_language
from src.main.util.consts import LOGGER_NAME, TASK, FILE_SYSTEM_ITEM, LANGUAGE
from src.main.util.file_util import get_all_file_system_items, remove_directory
from src.test.solution_space.solution_graph.util import get_two_vertices, init_default_ids
from src.main.solution_space.consts import GRAPH_FOLDER_PREFIX, FOLDER_WITH_CODE_FILES_FOR_TESTS, FILE_PREFIX

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
    return get_all_file_system_items(get_test_folder_path(), item_type=FILE_SYSTEM_ITEM.SUBDIR)


def get_actual_files_names(folder: str) -> List[str]:
    return get_all_file_system_items(os.path.join(get_test_folder_path(), folder))


def get_file_name(graph_id: int, code_id: int, graph_prefix: str = GRAPH_FOLDER_PREFIX, file_prefix: str = FILE_PREFIX,
                  language: LANGUAGE = LANGUAGE.PYTHON) -> str:
    return os.path.join(graph_prefix + str(graph_id), graph_prefix + str(graph_id) + '_' + file_prefix + str(code_id)
                        + str(get_extension_by_language(language).value))


def delete_folder() -> None:
    remove_directory(get_test_folder_path())


@pytest.mark.skipif(to_skip(current_module_level=TEST_LEVEL.SOLUTION_SPACE), reason=TEST_LEVEL.SOLUTION_SPACE.value)
class TestCodeToFile:

    # Create three graphs and check all folders names which were created for each graph
    def test_folders_names(self) -> None:
        delete_folder()
        init_default_ids()
        sg_0, sg_1, sg_2 = create_three_graphs()
        expected_folders_names = get_full_paths([GRAPH_FOLDER_PREFIX + '0',
                                                 GRAPH_FOLDER_PREFIX + '1',
                                                 NOT_DEFAULT_GRAPH_PREFIX + '2'])
        case = unittest.TestCase()
        case.assertCountEqual(expected_folders_names, get_actual_folders_names())

    def test_folder_structure_with_default_files_names(self) -> None:
        init_default_ids()
        sg_0, _, _ = create_three_graphs()
        vertices = get_two_vertices(sg_0)
        folder = GRAPH_FOLDER_PREFIX + str(sg_0.id)
        actual_files_names = get_actual_files_names(folder)

        expected_files_names = get_full_paths([get_file_name(sg_0.id, 0), get_file_name(sg_0.id, 1)])
        case = unittest.TestCase()
        case.assertCountEqual(expected_files_names, actual_files_names)

    def test_folder_structure_with_not_default_files_names(self) -> None:
        init_default_ids()
        _, sg_1, _ = create_three_graphs()
        vertices = get_two_vertices(sg_1)
        folder = GRAPH_FOLDER_PREFIX + str(sg_1.id)
        actual_files_names = get_actual_files_names(folder)

        expected_files_names = get_full_paths([get_file_name(sg_1.id, 0, file_prefix=NOT_DEFAULT_FILE_PREFIX),
                                               get_file_name(sg_1.id, 1, file_prefix=NOT_DEFAULT_FILE_PREFIX)])
        case = unittest.TestCase()
        case.assertCountEqual(expected_files_names, actual_files_names)

    def test_folder_structure_with_all_not_default_names(self) -> None:
        init_default_ids()
        _, _, sg_2 = create_three_graphs()
        vertices = get_two_vertices(sg_2)
        folder = os.path.join(get_test_folder_path(), NOT_DEFAULT_GRAPH_PREFIX + str(sg_2.id))
        actual_files_names = get_actual_files_names(folder)

        expected_files_names = get_full_paths([get_file_name(sg_2.id, 0, file_prefix=NOT_DEFAULT_FILE_PREFIX,
                                                             graph_prefix=NOT_DEFAULT_GRAPH_PREFIX),
                                               get_file_name(sg_2.id, 1, file_prefix=NOT_DEFAULT_FILE_PREFIX,
                                                             graph_prefix=NOT_DEFAULT_GRAPH_PREFIX)])
        case = unittest.TestCase()
        case.assertCountEqual(expected_files_names, actual_files_names)
