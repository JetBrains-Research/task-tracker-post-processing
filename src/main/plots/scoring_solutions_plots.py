# Copyright (c) by anonymous author(s)

from typing import List, Union, Tuple

import pandas as pd

from src.main.util.consts import ISO_ENCODING, CODE_TRACKER_COLUMN
from src.main.util.file_util import get_parent_folder, get_name_from_path
from src.main.preprocessing.code_anonimization import anonymize_code_in_df
from src.main.plots.util.graph_representation_util import get_color_by_rate, get_graph_representation, create_dot_graph


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


def plot_scoring_solutions(ct_file_path: str, name_prefix: str = 'scoring_solution') -> str:
    ct_df = pd.read_csv(ct_file_path, encoding=ISO_ENCODING)
    anon_ct_df = anonymize_code_in_df(ct_df)
    scores = anon_ct_df[CODE_TRACKER_COLUMN.TESTS_RESULTS.value].values
    labels, graph_structure = get_labels_and_graph_structure(scores)
    solutions_representation = get_graph_representation(labels, graph_structure)
    output_path = get_parent_folder(ct_file_path)
    output_path = create_dot_graph(output_path,
                                   f'{get_name_from_path(ct_file_path, False)}_{name_prefix}',
                                   solutions_representation)
    return output_path
