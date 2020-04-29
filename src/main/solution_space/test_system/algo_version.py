# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

from typing import Type



# # Todo: rename?
from src.main.solution_space.solution_graph import SolutionGraph



# class AlgoVersion():
#     def __init__(self, path_finder: Type[IPathFinder], measured_vertex: Type[IMeasuredVertex]):
#         self._path_finder = path_finder
#         self._measured_vertex = measured_vertex
#
#     @property
#     def path_finder(self) -> Type[IPathFinder]:
#         return self._path_finder
#
#     @property
#     def measured_vertex(self) -> Type[IMeasuredVertex]:
#         return self._measured_vertex
#
#     def create_path_finder(self, graph: SolutionGraph) -> IPathFinder:
#         return self._path_finder(graph, self._measured_vertex)
#
#     def __str__(self):
#         return f'path_finder\n:{self._path_finder.get_description()}\n' \
#                f'measured_vertex\n:{self._measured_vertex.get_description()}'
