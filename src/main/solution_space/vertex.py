# Copyright (c) by anonymous author(s)

from __future__ import annotations

import ast
from typing import List, Optional

import src.main.solution_space.solution_graph as sg
from src.main.solution_space.data_classes import CodeInfo
from src.main.canonicalization.ast_tools import AstStructure
from src.main.util.helper_classes.id_counter import IdCounter
from src.main.solution_space import consts as solution_space_consts
from src.main.util.helper_classes.pretty_string import PrettyString
from src.main.solution_space.serialized_code import Code, SerializedCode


class Vertex(IdCounter, PrettyString):

    def __init__(self, graph: sg.SolutionGraph, code: Optional[Code] = None, code_info: Optional[CodeInfo] = None,
                 vertex_type: solution_space_consts.VERTEX_TYPE = solution_space_consts.VERTEX_TYPE.INTERMEDIATE):
        self._parents = []
        self._children = []
        self._graph = graph
        self._serialized_code = None if code is None \
            else SerializedCode(code, code_info, graph.graph_directory, graph.file_prefix)
        self._vertex_type = vertex_type
        super().__init__(to_store_items=True)
        self.__init_nodes_numbers_and_structure()

    def __init_nodes_numbers_and_structure(self) -> None:
        if self._serialized_code is not None:
            canon_nodes_number = AstStructure.get_nodes_number_in_ast(self._serialized_code.canon_tree)
            self._graph.canon_nodes_number_dict[canon_nodes_number].append(self.id)
            for i, a_t in enumerate(self._serialized_code.anon_trees):
                self._graph.anon_nodes_number_dict[a_t.nodes_number].append((self.id, i))
                self._graph.anon_structure_dict[a_t.ast_structure].append(a_t.id)

    def add_anon_nodes_number_and_structure(self) -> None:
        last_index = len(self.serialized_code.anon_trees) - 1
        anon_tree = self.serialized_code.anon_trees[last_index]
        self.graph.anon_nodes_number_dict[anon_tree.nodes_number].append((self.id, last_index))
        self.graph.anon_structure_dict[anon_tree.ast_structure].append(anon_tree.id)


    @property
    def graph(self) -> sg.SolutionGraph:
        return self._graph

    @property
    def parents(self) -> List[Vertex]:
        return self._parents

    @property
    def children(self) -> List[Vertex]:
        return self._children

    @property
    def canon_tree(self) -> ast.AST:
        return self._serialized_code.canon_tree

    @property
    def serialized_code(self) -> SerializedCode:
        return self._serialized_code

    @property
    def vertex_type(self) -> solution_space_consts.VERTEX_TYPE:
        return self._vertex_type

    def __add_parent_to_list(self, parent: Vertex) -> None:
        self._parents.append(parent)

    def __add_child_to_list(self, child: Vertex) -> None:
        self._children.append(child)

    def add_child(self, child: Vertex) -> None:
        self.__add_child_to_list(child)
        child.__add_parent_to_list(self)

    def add_parent(self, parent: Vertex) -> None:
        self.__add_parent_to_list(parent)
        parent.__add_child_to_list(self)

    def get_dist(self, vertex: Vertex) -> int:
        return self._graph.dist.get_dist(self, vertex)

    def __str__(self) -> str:
        return f'Vertex id: {self._id}\n' \
               f'Vertex type: {self._vertex_type.value}\n' \
               f'Serialized_code: {self._serialized_code}\n' \
               f'Parents ids:\n{list(map(lambda parent: parent.id, self._parents))}\n' \
               f'Children:\n{list(map(lambda parent: parent.id, self._children))}'
