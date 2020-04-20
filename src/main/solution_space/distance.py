import ast
import logging
from abc import ABCMeta, abstractmethod
from typing import TypeVar, overload, List, Generic, Dict, Union

from functools import singledispatch
from src.main.solution_space.vertex import Vertex
from src.main.solution_space.code import SerializedCode
from src.main.canonicalization.diffs.gumtree_diff_handler import GumTreeDiffHandler
from src.main.util.consts import LOGGER_NAME
from src.main.util.log_util import log_and_raise_error
from src.main.canonicalization.canonicalization import get_code_from_tree

log = logging.getLogger(LOGGER_NAME)

Item = TypeVar('Item')
Upd = TypeVar('Upd')


# Todo: find a better way for distance implementation?

class IItemDistance(Generic[Item, Upd], metaclass=ABCMeta):
    def __init__(self):
        self._dist: Dict[Item, Dict[Item, int]] = {}

    def add_dist(self, new_item: Item) -> None:
        if new_item in self._dist.keys():
            log.info("This item already exists")
            return
        self._dist[new_item] = {}
        for old_item in self._dist.keys():
            self._dist[new_item][old_item] = self.find_dist(new_item, old_item)
            self._dist[old_item][new_item] = self.find_dist(old_item, new_item)

    def update_dist(self, upd_item: Item, updates: Upd) -> None:
        if upd_item not in self._dist.keys():
            log.info("This item doesn't exist, so dist cannot be updated")
            return
        for item in self._dist.keys():
            upd_dist = self.find_dist(item, updates)
            self._dist[item][upd_item] = min(self._dist[item][upd_item], upd_dist)
            upd_dist = self.find_dist(updates, item)
            self._dist[upd_item][item] = min(self._dist[upd_item][item], upd_dist)

    @abstractmethod
    def find_dist(self, src: Union[Item, Upd], dst: Union[Item, Upd]) -> int:
        raise NotImplementedError

# todo: rename arguments
class VertexDistance(IItemDistance[Vertex, str]):

    @singledispatch
    def find_dist(self, src: Vertex, dst: Vertex) -> int:
        src_anon_files = src.serialized_code.get_anon_files()
        src_canon_file = src.serialized_code.get_canon_file()
        dst_anon_files = dst.serialized_code.get_anon_files()
        dst_canon_file = dst.serialized_code.get_canon_file()
        
        canon_dist = GumTreeDiffHandler.get_diffs_number_with_gumtree(src_canon_file, dst_canon_file)
        anon_dist = self.__find_dist_between_files(src_anon_files, dst_anon_files)

        return min(canon_dist, anon_dist)

    @find_dist.register
    def _(self, src: str, dst: Vertex) -> int:
        anon_files = dst.serialized_code.get_anon_files()
        return self.__find_dist_between_files([src], anon_files)

    @find_dist.register
    def _(self, src: Vertex, dst: str) -> int:
        anon_files = src.serialized_code.get_anon_files()
        return self.__find_dist_between_files(anon_files, [dst])

    # todo: rename
    @staticmethod
    def __find_dist_between_files(src_files: List[str], dst_files: List[str]) -> int:
        diffs_numbers = []
        for src_file in src_files:
            for dst_file in dst_files:
                diffs_numbers.append(GumTreeDiffHandler.get_diffs_number_with_gumtree(src_file, dst_file))
        return min(diffs_numbers)


# @singledispatch
# def dist(src: Item, dst: Upd) -> int:
#     print("dist 7")
#     pass
#
#
# @dist.register
# def _(src_file: str, dst_file: str) -> int:
#     print("dist 6")
#     return GumTreeDiffHandler.get_diffs_number_with_gumtree(src_file, dst_file)
#
#
# @dist.register
# def _(src_files: list, dst_files: list) -> int:
#     print("dist 5")
#     diffs_numbers = []
#     for src_file in src_files:
#         for dst_file in dst_files:
#             diffs_numbers.append(dist(src_file, dst_file))
#     return min(diffs_numbers)
#
#
# @dist.register
# def _(src_code: SerializedCode, dst_code: SerializedCode) -> int:
#     print("dist 4")
#     src_anon_files = src_code.get_anon_files()
#     src_canon_file = src_code.get_canon_file()
#     dst_anon_files = dst_code.get_anon_files()
#     dst_canon_file = dst_code.get_canon_file()
#
#     return min(dist(src_canon_file, dst_canon_file), dist(src_anon_files, dst_anon_files))
#
#
# @dist.register
# def _(src_vertex: Vertex, dst_anon_file: str) -> int:
#     print("dist 3")
#     return dist(src_vertex.serialized_code.get_anon_files(), [dst_anon_file])
#
#
# @dist.register
# def _(src_anon_file: str, dst_vertex: Vertex) -> int:
#     print("dist 2")
#     return dist([src_anon_file], dst_vertex.serialized_code.get_anon_files())
#
#
# @dist.register
# def _(src_vertex: Vertex, dst_vertex: Vertex) -> int:
#     print("dist 1")
#     return dist(src_vertex.serialized_code, dst_vertex.serialized_code)
