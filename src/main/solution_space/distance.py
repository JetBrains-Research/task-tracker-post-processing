# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

from __future__ import annotations

import logging
import itertools
from queue import Queue
from threading import Thread
from abc import ABCMeta, abstractmethod
from typing import TypeVar, List, Generic, Dict, Union

from src.main.util.consts import LOGGER_NAME
from src.main.util.log_util import log_and_raise_error
from src.main.solution_space.solution_graph import Vertex
from src.main.util.helper_classes.id_counter import IdCounter
from src.main.canonicalization.diffs.gumtree import GumTreeDiff


log = logging.getLogger(LOGGER_NAME)

Item = TypeVar('Item', bound=IdCounter)
Upd = TypeVar('Upd')


class IDistanceMatrix(Generic[Item, Upd], metaclass=ABCMeta):
    _thread_number = 8

    # Todo: We should use multiprocessing (or Parallel), not multithreading.
    #  See https://timber.io/blog/multiprocessing-vs-multithreading-in-python-what-you-need-to-know/
    #  We'll change it as soon as we start using DistanceMatrix again
    class DistFiller(Thread, IdCounter):
        def __init__(self, queue: Queue, distance_matrix: IDistanceMatrix):
            super().__init__()
            log.info(f'Init {self.__class__.__name__} {self.id}')
            self._queue = queue
            self._dist_matrix = distance_matrix

        def run(self) -> None:
            while True:
                log.info(f'Run {self.__class__.__name__} {self.id}')
                src_item, dst_item = self._queue.get()
                try:
                    # It seems we don't need to lock anything since dict is thread safe as well as GumTreeDiff calling
                    dist = self._dist_matrix._IDistanceMatrix__find_dist(src_item, dst_item)
                    log.info(f'Found dist for src {src_item.id}, dst {dst_item.id} is {dist}')
                    self._dist_matrix._dist[src_item][dst_item] = dist
                    self._dist_matrix._dist[dst_item][src_item] = dist
                finally:
                    log.info(f'Task done by {self.__class__.__name__} {self.id}')
                    self._queue.task_done()

    def __init__(self, to_store_dist: bool = True):
        self._dist: Dict[Item, Dict[Item, int]] = {}
        self._to_store_dist = to_store_dist

    @property
    def to_store_dist(self) -> bool:
        return self._to_store_dist

    @to_store_dist.setter
    def to_store_dist(self, value: bool):
        log.info(f'Change to_store_dist from {self._to_store_dist} to {value}')
        # If we change to_store_dist from False to True, we need to fill dist dict
        if not self._to_store_dist and value:
            self.__fill_dist()
        self._to_store_dist = value

    # If we have stored a distance between src_item and dst_item, we return it, otherwise we find it explicitly.
    def get_dist(self, src_item: Item, dst_item: Item) -> int:
        dist = self._dist.get(src_item, {}).get(dst_item, None)
        #  If we don't store dist, dict can contain incorrect distances, so we should explicitly find it
        if not self._to_store_dist or dist is None:
            return self.__find_dist(src_item, dst_item)
        return dist

    def add_dist(self, new_item: Item) -> bool:
        if new_item in self._dist.keys():
            log.info('This item already exists')
            return False

        # If we don't store dist, we don't fill self._dist[new_item],
        # but we add an empty dict to be able to fill self._dist later
        self._dist[new_item] = {}
        if not self._to_store_dist:
            log.info('The param to_store_dist is False. We don\'t fill distance matrix')
            return False

        for old_item in self._dist.keys():
            dist = self.__find_dist(new_item, old_item)
            self._dist[new_item][old_item] = dist
            self._dist[old_item][new_item] = dist
        return True

    def update_dist(self, upd_item: Item, updates: Upd) -> bool:
        if not self._to_store_dist:
            log.info('The param to_store_dist is False. We don\'t update distance matrix')
            return False

        if upd_item not in self._dist.keys():
            log.info('This item doesn\'t exist, so dist cannot be updated')
            return False
        for item in self._dist.keys():
            # We can not get a distance less than 0
            if self._dist[item][upd_item] == 0:
                continue
            upd_dist = min(self._dist[item][upd_item], self.__find_updated_dist(item, updates))
            self._dist[item][upd_item] = upd_dist
            self._dist[upd_item][item] = upd_dist
        return True

    @abstractmethod
    def __find_dist(self, src: Item, dst: Item) -> int:
        raise NotImplementedError

    @abstractmethod
    def __find_updated_dist(self, src: Union[Item, Upd], dst: Union[Item, Upd]) -> int:
        raise NotImplementedError

    def __fill_dist(self) -> None:
        log.info(f'Start filling dist matrix, dict contains {len(self._dist.keys())} items')
        queue = Queue()
        for _ in range(self._thread_number):
            dist_finder = IDistanceMatrix.DistFiller(queue, self)
            dist_finder.daemon = True
            dist_finder.start()

        # Even if we didn't store dist, we added items as keys, so now we can fill dict
        for src_item, dst_item in itertools.combinations(self._dist.keys(), 2):
            queue.put((src_item, dst_item))
        queue.join()

    # Get matrix sorted according vertex ids
    def __get_dist_matrix(self) -> List[List[int]]:
        matrix = []
        for _, dst_vertices in sorted(self._dist.items(), key=(lambda item: item[0].id)):
            matrix.append([dist for _, dist in sorted(dst_vertices.items(), key=(lambda item: item[0].id))])
        return matrix


# We update 'Vertex' by adding new anon_file, so update type is 'str'
class VertexDistanceMatrix(IDistanceMatrix[Vertex, str]):

    def __init__(self, to_store_dist: bool = True):
        super().__init__(to_store_dist)

    # Need to add base class name as prefix if we want to have private abstract methods because otherwise
    # "TypeError: Can't instantiate abstract class ... with abstract methods ..." is raised.
    def _IDistanceMatrix__find_dist(self, src: Vertex, dst: Vertex) -> int:
        # Todo: it seems that GumTreeDiff always return 0 on the same fragments, but we need to add tests to be sure
        if src.id == dst.id:
            return 0

        src_anon_files = src.serialized_code.get_anon_files()
        src_canon_file = src.serialized_code.get_canon_file()
        dst_anon_files = dst.serialized_code.get_anon_files()
        dst_canon_file = dst.serialized_code.get_canon_file()
        
        canon_dist = GumTreeDiff.get_diffs_number(src_canon_file, dst_canon_file)
        # If canon_dist is a zero already, we cannot reduce the distance anymore, so we can return it without
        # finding diffs between anon trees
        if canon_dist == 0:
            return canon_dist
        anon_dist = self.__find_dist_between_files(src_anon_files, dst_anon_files)

        return min(canon_dist, anon_dist)

    # Singledispatch doesn't work for methods since it notes only the type of the first argument which is always 'self'
    # Multimethod doesn't work, because it raises an error:
    # AttributeError: 'multimethod' object has no attribute 'dispatch', and that's weird
    def _IDistanceMatrix__find_updated_dist(self, src: [Vertex, str], dst: [Vertex, str]) -> int:
        if isinstance(src, Vertex) and isinstance(dst, str):
            anon_files = src.serialized_code.get_anon_files()
            return self.__find_dist_between_files(anon_files, [dst])
        if isinstance(dst, Vertex) and isinstance(src, str):
            anon_files = dst.serialized_code.get_anon_files()
            return self.__find_dist_between_files([src], anon_files)
        else:
            log_and_raise_error(f'The function find_updated_dist is not implemented for types: src - {type(src)} and '
                                f'dst{type(src)}', log, NotImplementedError)

    @staticmethod
    def __find_dist_between_files(src_files: List[str], dst_files: List[str]) -> int:
        diffs_numbers = []

        for src_file, dst_file in itertools.product(src_files, dst_files):
            diffs_number = GumTreeDiff.get_diffs_number(src_file, dst_file)
            # If current diffs_number is a zero already, we cannot reduce the distance anymore
            if diffs_number == 0:
                return 0
            diffs_numbers.append(diffs_number)
        return min(diffs_numbers)
