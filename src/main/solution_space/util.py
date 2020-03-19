# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import os

from src.main.util import consts
from src.main.solution_space.consts import FOLDER_WITH_CODE_FILES, GRAPH_FOLDER_PREFIX


def get_graph_directory(graph_id: int, task: consts.TASK, graph_folder_prefix: str = GRAPH_FOLDER_PREFIX,
                        folder_with_code_files: str = FOLDER_WITH_CODE_FILES) -> str:
    return os.path.join(folder_with_code_files, task.value, graph_folder_prefix + str(graph_id))