# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

from __future__ import annotations

import os
import ast
import logging
from typing import Type, List, Optional
from abc import ABCMeta, abstractmethod

from src.main.util import consts
from src.main.util.file_util import create_file
from src.main.solution_space.serialized_code import AnonTree
from src.main.solution_space.solution_graph import SolutionGraph
from src.main.canonicalization.canonicalization import get_code_from_tree
from src.main.solution_space.measured_tree.measured_tree import IMeasuredTree

log = logging.getLogger(consts.LOGGER_NAME)


class IPathFinder(object, metaclass=ABCMeta):

    def __init__(self, graph: SolutionGraph, measured_vertex_subclass: Type[IMeasuredTree]):
        self._graph = graph
        self._measured_vertex_subclass = measured_vertex_subclass

    @property
    def graph(self) -> SolutionGraph:
        return self._graph

    @property
    def measured_vertex_subclass(self) -> Type[IMeasuredTree]:
        return self._measured_vertex_subclass

    def get_measured_tree(self, user_tree: AnonTree, candidate_tree: AnonTree) -> IMeasuredTree:
        return self._measured_vertex_subclass(user_tree, candidate_tree)

    # Find the next anon tree
    # Make sure code_info_list from user_anon_tree contains one code_info
    @abstractmethod
    def find_next_anon_tree(self, user_anon_tree: AnonTree, user_canon_tree: ast.AST,
                            candidates_file_id: Optional[str] = None) -> AnonTree:
        raise NotImplementedError

    def write_candidates_info_to_file(self, candidates: List[AnonTree], file_prefix: str = 'candidates',
                                      path: Optional[str] = None) -> str:
        candidates_info = ''.join([f'Tree id: {candidate.id}\n{get_code_from_tree(candidate.tree)}\n\n\n'
                                   for candidate in candidates])
        if path is None:
            path = os.path.join(self.graph.graph_directory, 'candidates_info')
        file_path = os.path.join(path, f'{file_prefix}_info{consts.EXTENSION.TXT.value}')
        create_file(candidates_info, file_path)
        log.info(f'Candidates were written in the file {file_path}')
        return file_path

    @staticmethod
    def get_file_prefix_by_user_tree(user_tree: AnonTree, file_id: Optional[int]) -> str:
        res = str(file_id) if file_id else ''
        return f'{res}_{user_tree.code_info_list[0].user.profile.age}' \
               f'_{user_tree.code_info_list[0].user.profile.experience}'
