# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import os
import pickle
import logging
from typing import Optional

from src.main.util.file_util import create_directory, is_file
from src.main.solution_space.solution_graph import SolutionGraph
from src.main.util.consts import SERIALIZED_GRAPH_PATH, EXTENSION, LOGGER_NAME


log = logging.getLogger(LOGGER_NAME)


class SolutionSpaceSerializer:

    # Returns file path with serialized graph
    @staticmethod
    def serialize(graph: SolutionGraph, serialized_file_prefix: str = 'serialized_graph') -> str:
        folder_path = os.path.join(SERIALIZED_GRAPH_PATH, f'graph_{graph.id}')
        create_directory(folder_path)
        file_path = os.path.join(folder_path, serialized_file_prefix + EXTENSION.PICKLE.value)
        with open(file_path, 'wb') as f:
            pickle.dump(graph, f, pickle.HIGHEST_PROTOCOL)
        log.info(f'Graph with id {graph.id} was serialized successfully. File path is {file_path}')
        return file_path

    @staticmethod
    def deserialize(path: str) -> Optional[SolutionGraph]:
        graph = None
        if not is_file(path):
            log.info(f'Path {path} is incorrect')
            return graph
        with open(path, 'rb') as f:
            graph = pickle.load(f)
        return graph
