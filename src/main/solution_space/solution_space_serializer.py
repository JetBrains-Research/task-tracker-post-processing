# Copyright (c) by anonymous author(s)

import os
import logging
from typing import Optional

from src.main.util.log_util import log_and_raise_error
from src.main.util.helper_classes.id_counter import IdCounter
from src.main.solution_space.solution_graph import SolutionGraph
from src.main.util.consts import SERIALIZED_GRAPH_PATH, EXTENSION, LOGGER_NAME
from src.main.util.file_util import is_file, serialize_data_and_write_to_file, deserialize_data_from_file, \
    remove_directory

log = logging.getLogger(LOGGER_NAME)


class SolutionSpaceSerializer:

    # Returns file path with serialized graph

    # While serializing a graph, please, don't run any additional unnecessary methods, especially which can change
    # IdCounter fields, because otherwise we'll serialize incorrect IdCounter instances and item_dict. If there were
    # any IdCounter objects, that don't belong to graph, their id will be in IdCounter, but the objects themselves won't
    # be serialized. So it can probably cause an error while getting item by id.
    @staticmethod
    def serialize(graph: SolutionGraph, serialized_file_suffix: str = 'serialized_graph') -> str:
        graph_name = f'graph_{graph.id}_{serialized_file_suffix}'
        graph_path = os.path.join(SERIALIZED_GRAPH_PATH, f'{graph_name}{EXTENSION.PICKLE.value}')
        objects_to_serialize = (graph, IdCounter._instances, IdCounter._id_item_dict_by_class)
        serialize_data_and_write_to_file(graph_path, objects_to_serialize)
        log.info(f'Graph with id {graph.id} was serialized successfully. File path is {graph_path}')
        return graph_path

    # While deserializing a graph, please, let it be the first action in the session, because deserialization replaces
    # all IdCounter fields. So all IdCounter objects that were created before deserialization will be lost.
    @staticmethod
    def deserialize(serialized_graph_path: str,
                    new_path_for_graph: Optional[str] = None,
                    to_delete_old_graph_directory: bool = True) -> Optional[SolutionGraph]:
        if not is_file(serialized_graph_path):
            log_and_raise_error(f'Path {serialized_graph_path} is incorrect', log)
        try:
            deserialized_graph, instances, item_dict =  deserialize_data_from_file(serialized_graph_path)
            IdCounter._instances = instances
            IdCounter._id_item_dict_by_class = item_dict
            if to_delete_old_graph_directory:
                remove_directory(deserialized_graph.graph_directory)
            deserialized_graph.recreate_graph_files(new_path_for_graph)
            return deserialized_graph
        except OSError:
            log_and_raise_error(f'OSError during the deserialized graph process. '
                                f'Serialized graph path is {serialized_graph_path}', log, OSError)
