# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import os
import logging
from typing import Optional

from src.main.solution_space.solution_graph import SolutionGraph
from src.main.util.consts import SERIALIZED_GRAPH_PATH, EXTENSION, LOGGER_NAME
from src.main.util.file_util import is_file, serialize_data_and_write_to_file, deserialize_data_from_file, \
    remove_directory
from src.main.util.log_util import log_and_raise_error

log = logging.getLogger(LOGGER_NAME)


class SolutionSpaceSerializer:

    # Returns file path with serialized graph
    @staticmethod
    def serialize(graph: SolutionGraph, serialized_file_prefix: str = 'serialized_graph') -> str:
        path = os.path.join(SERIALIZED_GRAPH_PATH, f'graph_{graph.id}_{serialized_file_prefix}{EXTENSION.PICKLE.value}')
        serialize_data_and_write_to_file(path, graph)
        log.info(f'Graph with id {graph.id} was serialized successfully. File path is {path}')
        return path

    @staticmethod
    def deserialize(serialized_graph_path: str,
                    new_path_for_graph: Optional[str] = None,
                    to_delete_old_graph_directory: bool = True) -> Optional[SolutionGraph]:
        if not is_file(serialized_graph_path):
            log.info(f'Path {serialized_graph_path} is incorrect')
            return None
        try:
            deserialized_graph: SolutionGraph = deserialize_data_from_file(serialized_graph_path)
        except OSError:
            log_and_raise_error(f'OSError during the deserialized graph process. Serialized graph path is '
                                f'{serialized_graph_path}', log, OSError)

        if to_delete_old_graph_directory:
            remove_directory(deserialized_graph.graph_directory)
        deserialized_graph.recreate_graph_files(new_path_for_graph)
        return deserialized_graph
