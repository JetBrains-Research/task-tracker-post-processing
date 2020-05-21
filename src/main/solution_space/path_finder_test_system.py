# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

from __future__ import annotations

import os
import ast
import logging
import inspect
import pkgutil
import importlib
import itertools
from enum import Enum
from abc import ABCMeta
from itertools import product
from types import FunctionType
from datetime import datetime, timedelta
from typing import Type, TypeVar, List, Dict, Any, Tuple, Optional

from prettytable import PrettyTable, ALL

from src.main.solution_space.hint import HintHandler
from src.main.solution_space.data_classes import Profile
from src.main.solution_space.serialized_code import AnonTree
from src.main.solution_space.solution_graph import SolutionGraph
from src.main.solution_space.path_finder.path_finder import IPathFinder
from src.main.canonicalization.canonicalization import get_code_from_tree
from src.main.solution_space.measured_tree.measured_tree import IMeasuredTree
from src.main.solution_space.consts import TEST_SYSTEM_GRAPH, SOLUTION_SPACE_FOLDER, TEST_SYSTEM_FRAGMENTS
from src.main.solution_space.solution_space_serializer import SolutionSpaceSerializer
from src.main.solution_space.solution_space_visualizer import SolutionSpaceVisualizer
from src.main.util.consts import LOGGER_NAME, INT_EXPERIENCE, TEST_RESULT, TASK, EXTENSION
from src.main.util.file_util import get_class_parent_package, create_file, add_suffix_to_file, \
    get_all_file_system_items, extension_file_condition, get_content_from_file
from src.main.util.log_util import log_and_raise_error

log = logging.getLogger(LOGGER_NAME)


# Todo: rewrite it
# Make sure 'INT_EXPERIENCE' is the last one, otherwise columns in result table will be in wrong order
class TEST_INPUT(Enum):
    SOURCE_CODE = 'source'
    RATE = 'rate'
    AGE = 'age'
    INT_EXPERIENCE = 'int_experience'


Class = TypeVar('Class')
TestInput = Dict[TEST_INPUT, Any]
# For class(as a key) stores a dict(as a value) with all class methods names(as keys), and class methods(as values)
MethodsDict = Dict[Type[Class], Dict[str, FunctionType]]


def skip(reason: str):
    def wrap(clazz: Type[Class]) -> None:
        clazz.is_skipped = True
        clazz.skipped_reason = reason

    return wrap


def doc_param(*sub):
    def wrap(obj):
        obj.__doc__ = obj.__doc__.format(*sub)
        return obj

    return wrap


# Print results of running all possible PathFinder and MeasuredVertex versions, using https://github.com/kxxoling/PTable
class TestSystem:
    _no_method_sign = '---'
    _spaces_to_crop_in_doc = 8

    def __init__(self, test_inputs: List[TestInput], graph: Optional[SolutionGraph] = None, task: Optional[TASK] = None,
                 serialized_graph_path: Optional[str] = TEST_SYSTEM_GRAPH, add_same_docs: bool = True,
                 to_visualize_graph: bool = True):

        # If task is not None, test_system tries to find serialized graph with name test_system_graph_task.pickle
        # in resources/test_system folder
        if task is not None:
            serialized_graph_path = add_suffix_to_file(serialized_graph_path, task.value)

        # If no graph is passed, test_system tries to deserialize graph from serialized_graph_path
        self._graph = graph if graph is not None else SolutionSpaceSerializer.deserialize(serialized_graph_path)

        if task and self._graph:
            assert self._graph.task == task

        if to_visualize_graph:
            s_v = SolutionSpaceVisualizer(self._graph)
            path = s_v.visualize_graph()
            log.info(f'Visualized graph path is {path}')
        # Maybe in the future we will be testing not only nex_anon_tree, but also the hints
        self._hint_handler = HintHandler(self._graph)
        self._add_same_docs = add_same_docs
        self._test_inputs = test_inputs
        self._path_finder_subclasses = self.__get_all_subclasses(IPathFinder)
        self._measured_vertex_subclasses = self.__get_all_subclasses(IMeasuredTree)
        TestSystem.__print_output(self.get_methods_doc_table(self._measured_vertex_subclasses,
                                                             'MeasuredVertex description',
                                                             ['__lt__']))
        TestSystem.__print_output(self.get_methods_doc_table(self._path_finder_subclasses, 'PathFinder description'))
        TestSystem.__print_output(self.get_result_table('Results of running find_next_vertex'),
                                  f'{self._graph.task.value}_result_table', True)

    # Get a table with all methods docs collected from given classes.
    # If some class doesn't have a method, there is self._no_method_sign (for example, '---') in a corresponding cell.
    # If some class does have a method, but without docs, there is an empty cell
    # +---------------+---------------+---------------+
    # |  class name   |    method_1   |    method_2   |
    # +---------------+---------------+---------------+
    # |    class_1    |               |     *doc*     |
    # +---------------+---------------+---------------+
    # |    class_2    |     *doc*     |     ---       |
    # +---------------+---------------+---------------+
    # methods_to_keep should contain object methods, which should be included in the table.
    # By default, all object methods are removed.
    def get_methods_doc_table(self, classes: List[Type[Class]], title: str,
                              methods_to_keep: Optional[List[str]] = None) -> Optional[PrettyTable]:
        if not classes:
            return None
        methods_dict, methods_names = self.__get_methods_dict_and_names(classes, methods_to_keep)
        table = PrettyTable(title=title)
        table.add_column('class_name', [c.__name__ for c in classes])
        for name in methods_names:
            methods = [methods_dict[c].get(name) for c in classes]
            docs = [self._no_method_sign if m is None else self.__format_doc_str(m.__doc__) for m in methods]
            if not self._add_same_docs and len(set(docs)) == 1:
                continue
            table.add_column(name, docs)

        return TestSystem.__set_table_style(table)

    # Get a table with all path_finder results for a given test_inputs:
    # +---------+-----+-------+---------------+---------------+
    # | ... input headers...  | path_finder_1 | path_finder_2 |
    # +---------+-----+-------+---------------+---------------+
    # |     test_input_1      |   *result*    |   *result*    |
    # +---------+-----+-------+---------------+---------------+
    # |     test_input_2      |   *result*    |   *result*    |
    # +---------+-----+-------+---------------+---------------+
    def get_result_table(self, title: str) -> Optional[PrettyTable]:
        path_finders = self.__get_all_possible_path_finders()
        if not path_finders:
            TestSystem.__print_output('There are no path_finders')
            return None
        # Set table headers: first go test_input headers, then path_finder versions
        table = PrettyTable(field_names=['index'] + [e.value for e in TEST_INPUT] +
                                        [self.__get_path_finder_version(pf) for pf in path_finders], title=title)

        log.info(f"There are {len(self._test_inputs)} test inputs")

        for i, test_input in enumerate(self._test_inputs):
            log.info(f"Running path finders on {i} test input")
            user_anon_tree, user_canon_tree = self.__create_user_trees(test_input)
            row = [i] + [test_input[key] for key in TEST_INPUT if key != TEST_INPUT.INT_EXPERIENCE] \
                  + [test_input[TEST_INPUT.INT_EXPERIENCE].get_str_experience()]
            for path_finder in path_finders:
                time, next_anon_tree = self.__run_path_finder(path_finder, user_anon_tree, user_canon_tree, i)
                hint = HintHandler.get_hint_by_anon_tree(test_input[TEST_INPUT.SOURCE_CODE], next_anon_tree)
                row.append(f'time: {time}'
                           f'\n\nnext anon tree id: {next_anon_tree.id}'
                           f'\n\nanon code:\n{get_code_from_tree(next_anon_tree.tree)}'
                           f'\n\napply diffs:\n{hint.recommended_code}')
            table.add_row(row)

        return TestSystem.__set_table_style(table)

    def __get_all_possible_path_finders(self) -> List[IPathFinder]:
        path_finders = []
        for pf_subclass, mv_subclass in product(self._path_finder_subclasses, self._measured_vertex_subclasses):
            path_finders.append(pf_subclass(self._graph, mv_subclass))
        return path_finders

    def __create_user_trees(self, test_input: TestInput) -> Tuple[AnonTree, ast.AST]:
        profile = Profile(test_input[TEST_INPUT.AGE], test_input[TEST_INPUT.INT_EXPERIENCE])
        # If rate is None, it's okay, it will be found further
        rate = test_input.get(TEST_INPUT.RATE)
        return self._hint_handler.create_user_trees(test_input[TEST_INPUT.SOURCE_CODE], profile, rate)

    @staticmethod
    def __run_path_finder(path_finder: IPathFinder, user_anon_tree: AnonTree, user_canon_tree: ast.AST,
                          candidates_file_id: int) -> Tuple[timedelta, AnonTree]:
        start_time = datetime.now()
        next_anon_tree = path_finder.find_next_anon_tree(user_anon_tree, user_canon_tree, candidates_file_id)
        end_time = datetime.now()
        return end_time - start_time, next_anon_tree

    # Gets path_finder version in format like this: 'PathFinderV1, MeasuredVertexV1'
    @staticmethod
    def __get_path_finder_version(path_finder: IPathFinder) -> str:
        return f'{type(path_finder).__name__}, {path_finder.measured_vertex_subclass.__name__}'

    @staticmethod
    def __format_doc_str(doc: str) -> str:
        lines = doc.split('\n')
        cropped_lines = [line[TestSystem._spaces_to_crop_in_doc:]
                         if line.startswith(TestSystem._spaces_to_crop_in_doc * ' ') else line for line in lines]
        return '\n'.join(cropped_lines)

    @staticmethod
    def __set_table_style(table: PrettyTable) -> PrettyTable:
        table.hrules = ALL
        table.align = 'l'
        return table

    # Filter all object methods like __new__,  __setattr__ except methods passed as argument
    # Filter ABCMeta class methods
    @staticmethod
    def __filter_method(method: FunctionType, object_methods_to_filter: Optional[List[str]]) -> bool:
        return not (method.__name__ in ABCMeta.__name__ or method.__name__ in object_methods_to_filter)

    @staticmethod
    def __get_class_methods_with_doc(clazz: Type[Class], methods_to_keep: Optional[List[str]]) -> List[FunctionType]:
        class_methods = [getattr(clazz, m) for m in dir(clazz) if callable(getattr(clazz, m))]
        object_methods_to_filter = [m for m in dir(object) if callable(getattr(object, m))]
        if methods_to_keep:
            object_methods_to_filter = [m for m in object_methods_to_filter if m not in methods_to_keep]
        filtered_class_methods = [m for m in class_methods if TestSystem.__filter_method(m, object_methods_to_filter)]
        return [m for m in filtered_class_methods if m.__doc__]

    # Get dict, that for each class stores a 'method by method name' dict, and list off all methods names
    @staticmethod
    def __get_methods_dict_and_names(classes: List[Type[Class]],
                                     methods_to_keep: Optional[List[str]]) -> Tuple[MethodsDict, List[str]]:
        methods_dict = {}
        methods_names = set()
        for c in classes:
            methods_dict[c] = {}
            class_methods = TestSystem.__get_class_methods_with_doc(c, methods_to_keep)
            for m in class_methods:
                methods_dict[c][m.__name__] = m
                methods_names.add(m.__name__)
        # Get sorted list to make it determined
        methods_names = sorted(methods_names)
        return methods_dict, methods_names

    @classmethod
    def __get_all_subclasses(cls, clazz: Type[Class]) -> List[Type[Class]]:
        # We need to import all subclasses modules before getting them:
        class_parent_package = get_class_parent_package(clazz)
        class_parent_dir = os.path.dirname(inspect.getfile(clazz))
        for (_, name, _) in pkgutil.iter_modules([class_parent_dir]):
            importlib.import_module(f'.{name}', class_parent_package)
        subclasses: list = clazz.__subclasses__()
        not_skipped_subclasses = subclasses.copy()
        for c in subclasses:
            if hasattr(c, 'is_skipped') and c.is_skipped:
                not_skipped_subclasses.remove(c)
                TestSystem.__print_output(f'{c.__name__} is skipped, reason: {c.skipped_reason}')
        return not_skipped_subclasses

    # Todo: add ability to print output to file?
    @staticmethod
    def __print_output(output: Optional[Any],
                       file_name: str = 'path_finder_test_system_output',
                       to_write_to_file: bool = False) -> None:
        if output is not None:
            print(f'{output}\n')
            if to_write_to_file:
                path = os.path.join(SOLUTION_SPACE_FOLDER, 'path_finder_test_system_output',
                                    file_name)
                extension = EXTENSION.HTML.value if isinstance(output, PrettyTable) else EXTENSION.TXT.value
                path += extension
                # todo: replace spaces to &nbsp;
                create_file(TestSystem.__format_content(output), path)

    @staticmethod
    def __format_content(output: Any) -> str:
        if not isinstance(output, PrettyTable):
            return output
        content = output.get_html_string(border=True, header=True, format=True)
        return content.replace('    ', '&nbsp;&nbsp;&nbsp;&nbsp;')

    @staticmethod
    def generate_all_test_fragments(ages: List[int], experiences: List[INT_EXPERIENCE],
                                    fragments: List[str]) -> List[Dict[TEST_INPUT, Any]]:
        return [{TEST_INPUT.SOURCE_CODE: f, TEST_INPUT.AGE: a,
                 TEST_INPUT.RATE: TEST_RESULT.CORRECT_CODE.value,
                 TEST_INPUT.INT_EXPERIENCE: e} for a, e, f in itertools.product(ages, experiences, fragments)]

    @staticmethod
    def get_fragments_for_task(task: TASK, path: str = TEST_SYSTEM_FRAGMENTS) -> List[str]:
        task_path = os.path.join(path, task.value)
        if os.path.exists(task_path):
            fragments = get_all_file_system_items(task_path, extension_file_condition(EXTENSION.PY))
            return list(map(get_content_from_file, fragments))

        if task == TASK.PIES:
            return ['a = int(input())',
                    'a = int(input())\nb = int(input())',
                    'a = int(input())\nb = int(input())\nn = int(input())',
                    'a = input()\nb = input()',
                    'a = 10\nb = 5\nn = 14\nprint(a * n,  b * n)',
                    'a = int(input())\nb = int(input())\nn = int(input())\nrub = a * n\ncop = b * n',
                    'a = int(input())\nb = int(input())\nn = int(input())\nrub = a * n\ncop = b * n\nprint(rub + " " + cop)',
                    'a = int(input())\nb = int(input())\nn = int(input())\nrub = a * n\ncop = b * n\nprint(str(rub) + " " + str(cop))',
                    'a = int(input())\nb = int(input())\nn = int(input())\nrub = a * n\nif b * n >= 100:\n    rub += b * n // 100',
                    'a = int(input())\nb = int(input())\nn = int(input())\nrub = a * n\nif b * n <= 100:\n    rub += b * n // 100',
                    'a = int(input())\nb = int(input())\nn = int(input())\nrub = a * n\nif b * n >= 100:\n    rub += b * n // 100\ncop = b * n\nprint(rub + " " + cop)',
                    'a = int(input())\nb = int(input())\nn = int(input())\nrub = a * n\ncop = b * n\nwhile cop > 100:\n    rub += 1',
                    'a = int(input())\nb = int(input())\nn = int(input())\nrub = a * n\ncop = b * n\nwhile cop > 100:\n    rub += 1\n    cop -= 100'
                    ]
        elif task == TASK.BRACKETS:
            return ['s = input()',
                    's = input()\nres = ""',
                    's = input()\nres = ""\nif len(s) % 2 == 0:\n    print(s)',
                    's = input()\nres = ""\nif len(s) % 2 == 0:\n    print(s)\nelse:\n    print(s)',
                    's = input()\nres = ""\nif len(s) % 2 == 0:\n    for i in range(len(s) // 2):\n        res += s[i] + "("',
                    's = input()\nres = ""\nif len(s) % 2 == 0:\n    for i in range(len(s) // 2):\n        res += s[i] + "("\n    for i in range(len(s) // 2 - 1, len(s)):\n        res += s[i] + ")"'
                    ]
        elif task == TASK.ZERO:
            return [
                'N = int(input())',
                'N = int(input())\nfor i in range(N):\n    a = int(input())',
                'N = int(input())\nfor i in range(N):\n    a = int(input())\n    if a == 0:\n        print("YES")',
                'N = int(input())\nfor i in range(N):\n    a = int(input())\n    if a == 0:\n        print("YES")\nprint("NO")',
                'N = int(input())\nc = 0\nfor i in range(N):\n    a = int(input())\n    if a == 0:\n        c += 1\nprint("NO")',
                'N = int(input())\nfor i in range(N):\n    a = int(input())\n    if a == 0:\n        nprint("YES")',
                'N = int(input())\nfor i in range(N):\n    a = int(input())\n    if a == 0:\n        nprint("YES")\nprint("NO")',
                'N = int(input())\nc = 0\nfor i in range(N):\n    a = int(input())\n    if a == 0:\n        c += 1\nif c > 0:\n    print("YES")',
                'N = int(input())\na = []\mfor i in range(N):\n    c = int(input())',
                'N = int(input())\na = []\mfor i in range(N):\n    c = int(input())\n    a.append(c)',
                'N = int(input())\na = []\mfor i in range(N):\n    c = int(input())\n    a.append(c)\na.sort()',
                'N = int(input())\na = []\mfor i in range(N):\n    c = int(input())\n    a.append(c)\na.sort()\nif a[0] == 0:\n    print("YES")',
                'N = int(input())\na = []\mfor i in range(N):\n    c = int(input())\n    a.append(c)\na.sort()\nif a[0] != 0:\n    print("NO")',
                'N = int(input())\na = []\mfor i in range(N):\n    c = int(input())\n    a.append(c)\nm = min(a)\nif m == 0:\n    print("YES")',
                'N = int(input())\na = []\mfor i in range(N):\n    c = int(input())\n    a.append(c)\nm = min(a)\nif m != 0:\n    print("NO")'
            ]
        elif task == TASK.MAX_3:
            return [
                'a = int(input())',
                'a = int(input())\nb = int(input())',
                'a = int(input())\nb = int(input())\nc = int(input())',
                'a = int(input())\nb = int(input())\nc = int(input())\nif a > b and a > c:\n    print(a)',
                'a = int(input())\nb = int(input())\nc = int(input())\nm = a',
                'a = int(input())\nb = int(input())\nc = int(input())\nm = a\nif b > m:\n    m = b\nif c > m:\n    m = c',
                'a = int(input())\nb = int(input())\nc = int(input())\nk = []',
                'a = int(input())\nb = int(input())\nc = int(input())\nk = []\nk.append(a)',
                'a = int(input())\nb = int(input())\nc = int(input())\nk = []\nk.append(a)\nk.append(b)',
                'a = int(input())\nb = int(input())\nc = int(input())\nk = []\nk.append(a)\nk.append(b)\nk.append(c)',
                'a = int(input())\nb = int(input())\nc = int(input())\nk = [a, b, c]',
                'a = int(input())\nb = int(input())\nc = int(input())\nif a > b and a > c:\n    print(a)\nelif a == b == c:\n    print(a)',
                'a = int(input())\nb = int(input())\nc = int(input())\nif a > b and a > c:\n    print(a)\nelif a == b == c:\n    print(a)\nelif b > a and b < c:\n    print(c)'
            ]
        else:
            log_and_raise_error(f'No fragments found in path {task_path}', log, NotImplementedError)

