# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

from typing import List, Union, Tuple

import pandas as pd

from src.main.util import consts
from src.main.task_scoring.task_scoring import unpack_tests_results
from src.main.util.consts import ISO_ENCODING, CODE_TRACKER_COLUMN, TEST_RESULT, TASK
from src.main.util.file_util import get_parent_folder, get_name_from_path
from src.main.plots.util.graph_representation_util import get_color_by_rate, get_graph_representation, create_dot_graph

TESTS_RESULTS = consts.CODE_TRACKER_COLUMN.TESTS_RESULTS.value
FILE_NAME = consts.CODE_TRACKER_COLUMN.FILE_NAME.value


def __find_next_score_index(scores: List[float], start_index: int = 0) -> int:
    for i in range(start_index, len(scores)):
        if scores[i] != scores[start_index]:
            return i
    return len(scores)


def __get_label_for_score(id: int, label: Union[str, int], score: float) -> str:
    return f'{id} [label="{label}", style=filled, fillcolor={get_color_by_rate(score)}]\n'


def __get_edge(src_id: int, dst_id: int) -> str:
    return f'{src_id} -> {dst_id}\n'


def get_labels_and_graph_structure(scores: List[float]) -> Tuple[str, str]:
    labels = ''
    structure = ''
    i = 0
    while i < len(scores):
        next_score_index = __find_next_score_index(scores, i)
        # Collapse long chains of vertices with the same score

        # Add the current vertex
        labels += __get_label_for_score(i + 1, i + 1, scores[i])
        # If the current vertex is not the first, add en edge with the previous one
        if i != 0:
            structure += __get_edge(i, i + 1)

        # If we need to add an intermediate vertex
        if i < next_score_index - 2:
            # Add an intermediate vertex
            labels += __get_label_for_score(i + 2, '...', scores[i])
            structure += __get_edge(i + 1, i + 2)

            labels += __get_label_for_score(next_score_index, next_score_index, scores[i])
            structure += __get_edge(i + 2, next_score_index)
            i = next_score_index - 1

        i += 1
    return labels, structure


def __is_incorrect_fragment(tests_results: str) -> bool:
    return TEST_RESULT.INCORRECT_CODE.value in unpack_tests_results(tests_results, TASK.tasks())


def calculate_current_task_rate(df: pd.DataFrame) -> pd.DataFrame:
    file_name = df[FILE_NAME].unique()[0]
    current_task = TASK(get_name_from_path(file_name, False))
    return df[TESTS_RESULTS].apply(lambda x: unpack_tests_results(x, TASK.tasks())[TASK.tasks().index(current_task)])


# For more details see https://github.com/JetBrains-Research/codetracker-data/wiki/Visualization:-scoring-solutions-plots
def plot_scoring_solutions(ct_file_path: str, name_prefix: str = 'scoring_solution') -> str:
    ct_df = pd.read_csv(ct_file_path, encoding=ISO_ENCODING)
    # Delete incorrect fragments
    correct_df = ct_df[ct_df.apply(lambda row: not __is_incorrect_fragment(row[TESTS_RESULTS]), axis=1)]

    correct_df[TESTS_RESULTS] = calculate_current_task_rate(correct_df)
    scores = correct_df[CODE_TRACKER_COLUMN.TESTS_RESULTS.value].values
    labels, graph_structure = get_labels_and_graph_structure(scores)
    solutions_representation = get_graph_representation(labels, graph_structure)
    output_path = get_parent_folder(ct_file_path)
    output_path = create_dot_graph(output_path,
                                   f'{get_name_from_path(ct_file_path, False)}_{name_prefix}',
                                   solutions_representation)
    return output_path
