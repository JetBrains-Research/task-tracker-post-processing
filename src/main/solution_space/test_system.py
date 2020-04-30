# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

from __future__ import annotations

import os
import time
import inspect
import pkgutil
import importlib
from abc import ABCMeta
from datetime import datetime
from enum import Enum
from types import FunctionType
from typing import Type, TypeVar, List, Dict, Any, Tuple

from prettytable import PrettyTable, ALL

from src.main.util.consts import EXPERIENCE, LOGGER_NAME
from src.main.solution_space.serialized_code import Code
from src.main.solution_space.solution_graph import Vertex
from src.main.util.file_util import get_class_parent_package
from src.main.solution_space.consts import TEST_SYSTEM_GRAPH
from src.main.solution_space.path_finder.path_finder import IPathFinder
from src.main.solution_space.data_classes import CodeInfo, User, Profile
from src.main.util.log_util import log_and_raise_error, configure_logger
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


# Print results of running all possible PathFinder and MeasuredVertex versions, using https://github.com/kxxoling/PTable
class TestSystem:
    _no_method_sign = '---'

    def __init__(self, test_inputs: List[TestInput], serialized_graph_path: str = TEST_SYSTEM_GRAPH):
        graph = SolutionSpaceSerializer.deserialize(serialized_graph_path)
        if graph is None:
            log_and_raise_error('Deserialization failed, returned graph is None', log)
        self._graph = graph
        self._test_inputs = test_inputs
        self._path_finder_subclasses = self.__get_all_subclasses(IPathFinder)
        self._measured_vertex_subclasses = self.__get_all_subclasses(IMeasuredVertex)
        print(self.get_method_doc_table(self._measured_vertex_subclasses, 'MeasuredVertex description'))
        print(self.get_method_doc_table(self._path_finder_subclasses, 'PathFinder description'))
        print(self.get_result_table('Results of running find_next_vertex'))

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
    @staticmethod
    def get_method_doc_table(classes: List[Type[Class]], title: str) -> PrettyTable:
        methods_dict, methods_names = TestSystem.__get_methods_dict_and_names(classes)
        table = PrettyTable(field_names=['class name'] + methods_names, title=title)
        for c in classes:
            class_row = [c.__name__]
            for name in methods_names:
                method = methods_dict[c].get(name)
                doc = TestSystem._no_method_sign if method is None else TestSystem.__format_doc_str(method.__doc__)
                class_row.append(doc)
            table.add_row(class_row)
        return TestSystem.__set_table_style(table)

    # Get a table with all path_finder results for a given test_inputs:
    # +---------+-----+-------+---------------+---------------+
    # | ... input headers...  | path_finder_1 | path_finder_2 |
    # +---------+-----+-------+---------------+---------------+
    # |     test_input_1      |   *result*    |   *result*    |
    # +---------+-----+-------+---------------+---------------+
    # |     test_input_2      |   *result*    |   *result*    |
    # +---------+-----+-------+---------------+---------------+
    def get_result_table(self, title: str) -> PrettyTable:
        path_finders = self.__get_all_possible_path_finders()
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
        for path_finder_subclass in self._path_finder_subclasses:
            for measured_vertex_subclass in self.__get_all_subclasses(IMeasuredVertex):
                path_finders.append(path_finder_subclass(self._graph, measured_vertex_subclass))
        return path_finders

    def __create_user_vertex(self, test_input: TestInput) -> Vertex:
        # todo: find rate
        rate = 0
        vertex = Vertex(self._graph, Code.from_source(test_input[TEST_INPUT.SOURCE_CODE], rate))
        code_info = CodeInfo(User(Profile(test_input[TEST_INPUT.AGE], test_input[TEST_INPUT.EXPERIENCE])))
        vertex.add_code_info(code_info)
        return vertex

    @staticmethod
    def __run_path_finder(path_finder: IPathFinder, user_vertex: Vertex) -> str:
        # time_format = '%m/%d/%y %H:%M:%S'
        start_time = datetime.now()
        next_vertex = path_finder.find_next_vertex(user_vertex)
        end_time = datetime.now()
        return f'time: {end_time - start_time}\n\n' \
               f'vertex id: {next_vertex.id}\n\n' \
               f'canon code:\n{get_code_from_tree(next_vertex.canon_tree)}'

    # Gets path_finder version in format like this: 'PathFinderV1, MeasuredVertexV1'
    @staticmethod
    def __get_path_finder_version(path_finder: IPathFinder) -> str:
        return f'{type(path_finder).__name__},{path_finder.measured_vertex_subclass.__name__}'

    @staticmethod
    def __format_doc_str(doc: str) -> str:
        spaces_to_remove = 8
        lines = doc.split('\n')
        lines = [l[spaces_to_remove:] for l in lines if l.startswith(spaces_to_remove * ' ')]
        return '\n'.join(lines)

    @staticmethod
    def __set_table_style(table: PrettyTable) -> PrettyTable:
        table.hrules = ALL
        table.align = 'l'
        return table

    # Filter methods to get rid of different '__dir__'-like methods or '<class> ABCMeta'
    @staticmethod
    def __filter_method(method: FunctionType) -> bool:
        return not ((method.__name__.startswith('__') and method.__name__.endswith('__')) or isinstance(method, ABCMeta))

    @staticmethod
    def __get_class_methods_with_doc(clazz: Type[Class]) -> List[FunctionType]:
        class_methods = [getattr(clazz, m) for m in dir(clazz) if callable(getattr(clazz, m))]
        filtered_class_methods = [m for m in class_methods if TestSystem.__filter_method(m)]
        return [m for m in filtered_class_methods if m.__doc__]

    # Get dict, that for each class stores a 'method by method name' dict, and list off all methods names
    @staticmethod
    def __get_methods_dict_and_names(classes: List[Type[Class]]) -> Tuple[MethodsDict, List[str]]:
        methods_dict = {}
        methods_names = set()
        for c in classes:
            methods_dict[c] = {}
            class_methods = TestSystem.__get_class_methods_with_doc(c)
            for m in class_methods:
                methods_dict[c][m.__name__] = m
                methods_names.add(m.__name__)
        # Get sorted list to make it determined
        methods_names = sorted(methods_names)
        methods_names.remove('ABCMeta')
        return methods_dict, methods_names

    @classmethod
    def __get_all_subclasses(cls, clazz: Type[Class]) -> List[Type[Class]]:
        # We need to import all subclasses modules before getting them:
        class_parent_package = get_class_parent_package(clazz)
        class_parent_dir = os.path.dirname(inspect.getfile(clazz))
        for (_, name, _) in pkgutil.iter_modules([class_parent_dir]):
            importlib.import_module(f'.{name}', class_parent_package)
        return clazz.__subclasses__()


configure_logger()
test_fragments = [{TEST_INPUT.SOURCE_CODE: 'a = int(input())',
                   TEST_INPUT.AGE: 17,
                   TEST_INPUT.EXPERIENCE: EXPERIENCE.LESS_THAN_HALF_YEAR},
                  {TEST_INPUT.SOURCE_CODE: 'a = int(input())\nb = int(input())',
                   TEST_INPUT.AGE: 12,
                   TEST_INPUT.EXPERIENCE: EXPERIENCE.FROM_ONE_TO_TWO_YEARS}]

ts = TestSystem(test_fragments)
