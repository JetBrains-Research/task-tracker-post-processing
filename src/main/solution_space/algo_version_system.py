# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina
import logging
import os
import pkgutil
import importlib
from enum import Enum
from typing import Type, List, TypeVar, Union

from src.main.canonicalization.canonicalization import get_code_from_tree
from src.main.solution_space.code_1 import Code
from src.main.solution_space.data_classes import CodeInfo, User, Profile
from src.main.solution_space.hint import HintHandler
from src.main.util import consts
from src.main.util.consts import TASK, LOGGER_NAME, EXPERIENCE, DEFAULT_VALUE
from src.main.solution_space.algo_version import AlgoVersion
from src.main.solution_space.solution_graph import SolutionGraph, Vertex
from src.main.solution_space.path_finder.path_finder import IPathFinder
from src.main.solution_space.measured_vertex.measured_vertex import IMeasuredVertex

# File cannot be named 'test_system.py' because of pytest

log = logging.getLogger(LOGGER_NAME)

Class = TypeVar('Class')


task = TASK.PIES
# Todo: Deserialize graph
graph = SolutionGraph(task)


# To make '__subclasses__()' work all subclasses need to be imported
def get_all_subclasses(clazz: Type[Class]):
    module = clazz.__module__
    pkg_dir = os.path.dirname(clazz.__module__)
    for (module_loader, name, ispkg) in pkgutil.iter_modules([pkg_dir]):
        importlib.import_module(name)
    return clazz.__subclasses__()


def create_user_vertex(source_code: str, age: int, experience: Union[EXPERIENCE, DEFAULT_VALUE]) -> Vertex:
    # todo: find rate
    rate = 0
    vertex = Vertex(graph, Code.from_source(source_code, rate))
    code_info = CodeInfo(User(Profile(age, experience)))
    vertex.add_code_info(code_info)
    return vertex


algo_versions = []
m = IPathFinder.__module__
dir = os.path.dirname(m)
for path_finder in get_all_subclasses(IPathFinder):
    for measured_vertex in get_all_subclasses(IMeasuredVertex):
        algo_versions.append(AlgoVersion(path_finder, measured_vertex))


# Todo: Add more code fragments, change their structure?
test_fragments = [['a = int(input())', 12, EXPERIENCE.LESS_THAN_HALF_YEAR],

                  ['a = int(input())\n'
                   'b = int(input())', 28, EXPERIENCE.MORE_THAN_SIX],

                  ['c = 5', 20, EXPERIENCE.FROM_ONE_TO_TWO_YEARS]]


for source_code, age, experience in test_fragments:
    log.info(f'Fragments is:\n{source_code}')
    user_vertex = create_user_vertex(source_code, age, experience)
    for algo_versions in algo_versions:
        log.info(f'Algo version: {algo_versions}')
        path_finder = algo_versions.create_path_finder(graph)
        next_vertex = path_finder.find_next_vertex(user_vertex)
        # log.info(f'Next vertex is: vertex {next_vertex.id} with source_code:\n{get_code_from_tree(next_vertex.canon_tree)}')
