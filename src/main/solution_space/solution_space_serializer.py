# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import os
import logging
from typing import Optional

from src.main.solution_space.solution_graph import SolutionGraph
from src.main.util.consts import SERIALIZED_GRAPH_PATH, EXTENSION, LOGGER_NAME
from src.main.util.file_util import is_file, serialize_data_and_write_to_file, deserialize_data_from_file


log = logging.getLogger(LOGGER_NAME)


class SolutionSpaceSerializer:

    # Returns file path with serialized graph
    @staticmethod
    def serialize(graph: SolutionGraph, serialized_file_prefix: str = 'serialized_graph') -> str:
        path = os.path.join(SERIALIZED_GRAPH_PATH, f'graph_{graph.id}',
                            serialized_file_prefix + EXTENSION.PICKLE.value)
        serialize_data_and_write_to_file(path, graph)
        log.info(f'Graph with id {graph.id} was serialized successfully. File path is {path}')
        return path

    @staticmethod
    def deserialize(path: str) -> Optional[SolutionGraph]:
        if not is_file(path):
            log.info(f'Path {path} is incorrect')
            return None
        return deserialize_data_from_file(path)
