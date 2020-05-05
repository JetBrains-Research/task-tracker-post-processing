# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

from __future__ import annotations

import os
import inspect
import pkgutil
import importlib
from enum import Enum
from abc import ABCMeta
from datetime import datetime
from itertools import product
from types import FunctionType
from typing import Type, TypeVar, List, Dict, Any, Tuple, Optional

from prettytable import PrettyTable, ALL

from src.main.util.consts import LOGGER_NAME
from src.main.solution_space.serialized_code import Code
from src.main.solution_space.solution_graph import Vertex
from src.main.util.file_util import get_class_parent_package
from src.main.solution_space.consts import TEST_SYSTEM_GRAPH
from src.main.solution_space.path_finder.path_finder import IPathFinder
from src.main.solution_space.data_classes import CodeInfo, User, Profile
from src.main.canonicalization.canonicalization import get_code_from_tree, logging
from src.main.solution_space.measured_vertex.measured_vertex import IMeasuredVertex
from src.main.solution_space.solution_space_serializer import SolutionSpaceSerializer

log = logging.getLogger(LOGGER_NAME)


class TEST_INPUT(Enum):
    SOURCE_CODE = 'source'
    AGE = 'age'
    EXPERIENCE = 'experience'


Class = TypeVar('Class')
TestInput = Dict[TEST_INPUT, Any]
# For class(as a key) stores a dict(as a value) with all class methods names(as keys), and class methods(as values)
MethodsDict = Dict[Type[Class], Dict[str, FunctionType]]


def skip(reason: str):
    def wrap(clazz: Type[Class]) -> None:
        clazz.is_skipped = True
        clazz.skipped_reason = reason
    return wrap


# Print results of running all possible PathFinder and MeasuredVertex versions, using https://github.com/kxxoling/PTable
class TestSystem:
    _no_method_sign = '---'
    _spaces_to_crop_in_doc = 8

    def __init__(self, test_inputs: List[TestInput], serialized_graph_path: str = TEST_SYSTEM_GRAPH,
                 add_same_docs: bool = True):
        graph = SolutionSpaceSerializer.deserialize(serialized_graph_path)
        self._graph = graph
        self._add_same_docs = add_same_docs
        self._test_inputs = test_inputs
        self._path_finder_subclasses = self.__get_all_subclasses(IPathFinder)
        self._measured_vertex_subclasses = self.__get_all_subclasses(IMeasuredVertex)
        TestSystem.__print_output(self.get_methods_doc_table(self._measured_vertex_subclasses,
                                                             'MeasuredVertex description',
                                                             ['__lt__']))
        TestSystem.__print_output(self.get_methods_doc_table(self._path_finder_subclasses, 'PathFinder description'))
        TestSystem.__print_output(self.get_result_table('Results of running find_next_vertex'))

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
        table = PrettyTable(field_names=[e.value for e in TEST_INPUT] +
                                        [self.__get_path_finder_version(pf) for pf in path_finders], title=title)

        for test_input in self._test_inputs:
            user_vertex = self.__create_user_vertex(test_input)
            row = [test_input[key] for key in TEST_INPUT]
            for path_finder in path_finders:
                row.append(self.__run_path_finder(path_finder, user_vertex))
            table.add_row(row)

        return TestSystem.__set_table_style(table)

    def __get_all_possible_path_finders(self) -> List[IPathFinder]:
        path_finders = []
        for pf_subclass, mv_subclass in product(self._path_finder_subclasses, self._measured_vertex_subclasses):
            path_finders.append(pf_subclass(self._graph, mv_subclass))
        return path_finders

    def __create_user_vertex(self, test_input: TestInput) -> Vertex:
        vertex = Vertex(self._graph, Code.from_source(test_input[TEST_INPUT.SOURCE_CODE], None, self._graph.task))
        # Todo: init profile if it's None
        code_info = CodeInfo(User(Profile(test_input[TEST_INPUT.AGE], test_input[TEST_INPUT.EXPERIENCE])))
        vertex.add_code_info(code_info)
        return vertex


    @staticmethod
    def __run_path_finder(path_finder: IPathFinder, user_vertex: Vertex) -> str:
        start_time = datetime.now()
        next_vertex = path_finder.find_next_vertex(user_vertex)
        end_time = datetime.now()
        return f'time: {end_time - start_time}\n\n' \
               f'vertex id: {next_vertex.id}\n\n' \
               f'canon code:\n{get_code_from_tree(next_vertex.canon_tree)}'

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
    def __filter_method(method: FunctionType, object_methods_to_keep: Optional[List[str]]) -> bool:
        object_methods_to_filter = [m for m in dir(object) if callable(getattr(object, m))]
        if object_methods_to_keep:
            object_methods_to_filter = [m for m in object_methods_to_filter if m not in object_methods_to_keep]
        return not (method.__name__ in ABCMeta.__name__ or method.__name__ in object_methods_to_filter)

    @staticmethod
    def __get_class_methods_with_doc(clazz: Type[Class], methods_to_keep: Optional[List[str]]) -> List[FunctionType]:
        class_methods = [getattr(clazz, m) for m in dir(clazz) if callable(getattr(clazz, m))]
        filtered_class_methods = [m for m in class_methods if TestSystem.__filter_method(m, methods_to_keep)]
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
    def __print_output(output: Optional[Any]) -> None:
        if output is not None:
            print(f'{output}\n')
