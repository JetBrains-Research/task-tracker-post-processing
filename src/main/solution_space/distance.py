# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import itertools
import logging
from abc import ABCMeta, abstractmethod
from typing import TypeVar, List, Generic, Dict, Union, Type

from src.main.util.consts import LOGGER_NAME
from src.main.solution_space.solution_graph import Vertex
from src.main.canonicalization.diffs.gumtree_diff_handler import GumTreeDiffHandler
from src.main.util.log_util import log_and_raise_error

log = logging.getLogger(LOGGER_NAME)

Item = TypeVar('Item')
Upd = TypeVar('Upd')


class IDistanceMatrix(Generic[Item, Upd], metaclass=ABCMeta):
    def __init__(self, to_store_dist: bool = True):
        # Todo: is it better to use id as a key instead of Item?
        self._dist: Dict[Item, Dict[Item, int]] = {}
        self._to_store_dist = to_store_dist

    # If we have stored a distance between src_item and dst_item, we return it, otherwise we find it explicitly.
    def get_dist(self, src_item: Item, dst_item: Item) -> int:
        dist = self._dist.get(src_item, {}).get(dst_item, None)
        if dist is None:
            return self.__find_dist(src_item, dst_item)
        return dist

    def add_dist(self, new_item: Item) -> bool:
        if not self._to_store_dist:
            log.info('The param to_store_dist is False. We don\'t use distance matrix')
            return False

        if new_item in self._dist.keys():
            log.info('This item already exists')
            return False
        self._dist[new_item] = {}
        for old_item in self._dist.keys():
            self._dist[new_item][old_item] = self.__find_dist(new_item, old_item)
            self._dist[old_item][new_item] = self.__find_dist(old_item, new_item)
        return True

    def update_dist(self, upd_item: Item, updates: Upd) -> bool:
        if not self._to_store_dist:
            log.info('The param to_store_dist is False. We don\'t use distance matrix')
            return False

        if upd_item not in self._dist.keys():
            log.info('This item doesn\'t exist, so dist cannot be updated')
            return False
        for item in self._dist.keys():
            upd_dist = self.__find_updated_dist(item, updates)
            self._dist[item][upd_item] = min(self._dist[item][upd_item], upd_dist)
            upd_dist = self.__find_updated_dist(updates, item)
            self._dist[upd_item][item] = min(self._dist[upd_item][item], upd_dist)
        return True

    @abstractmethod
    def __find_dist(self, src: Item, dst: Item) -> int:
        raise NotImplementedError

    @abstractmethod
    def __find_updated_dist(self, src: Union[Item, Upd], dst: Union[Item, Upd]) -> int:
        raise NotImplementedError

    def __get_dist_matrix(self) -> List[List[int]]:
        return [list(d.values()) for d in self._dist.values()]


# Todo: add somewhere method to find distance between Vertex and Code. Will decide it in the next PR
#  with algo versions because it's needed only there

# We update 'Vertex' by adding new anon_file, so update type is 'str'
class VertexDistanceMatrix(IDistanceMatrix[Vertex, str]):

    def __init__(self, to_store_dist: bool = True):
        super().__init__(to_store_dist)

    # Need to add base class name as prefix if we want to have private abstract methods because otherwise
    # "TypeError: Can't instantiate abstract class ... with abstract methods ..." is raised.
    def _IDistanceMatrix__find_dist(self, src: Vertex, dst: Vertex) -> int:
        # Todo: it seems that GumTreeDiff always return 0 on the same fragments, but we need to add tests to be sure
        if src == dst:
            return 0

        src_anon_files = src.serialized_code.get_anon_files()
        src_canon_file = src.serialized_code.get_canon_file()
        dst_anon_files = dst.serialized_code.get_anon_files()
        dst_canon_file = dst.serialized_code.get_canon_file()
        
        canon_dist = GumTreeDiffHandler.get_diffs_number_with_gumtree(src_canon_file, dst_canon_file)
        # If canon_dist is a zero already, we cannot reduce the distance anymore, so we can return it without
        # finding diffs between anon trees
        if canon_dist == 0:
            return canon_dist
        anon_dist = self.__find_dist_between_files(src_anon_files, dst_anon_files)

        return min(canon_dist, anon_dist)

    # Todo: make it better?
    # Singledispatch doesn't work for methods since it notes only the type of the first argument which is always 'self'
    # Multimethod doesn't work, because it raises an error:
    # AttributeError: 'multimethod' object has no attribute 'dispatch', and that's weird
    # Is it better to split it into two methods with different names?
    def _IDistanceMatrix__find_updated_dist(self, src: [Vertex, str], dst: [Vertex, str]) -> int:
        if isinstance(src, Vertex) and isinstance(dst, str):
            anon_files = src.serialized_code.get_anon_files()
            return self.__find_dist_between_files(anon_files, [dst])
        if isinstance(dst, Vertex) and isinstance(src, str):
            anon_files = dst.serialized_code.get_anon_files()
            return self.__find_dist_between_files([src], anon_files)
        else:
            log_and_raise_error(f'The function find_updated_dist does not implemented for types: src - {type(src)} and '
                                f'dst{type(src)}', log, NotImplementedError)

    @staticmethod
    def __find_dist_between_files(src_files: List[str], dst_files: List[str]) -> int:
        diffs_numbers = []
        for src_file, dst_file in itertools.product(src_files, dst_files):
            diffs_number = GumTreeDiffHandler.get_diffs_number_with_gumtree(src_file, dst_file)
            diffs_numbers.append(diffs_number)
        return min(diffs_numbers)
