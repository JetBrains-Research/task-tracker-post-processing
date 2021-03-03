# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

from src.main.processing.coding_assistant_processing.delete_unnecessary_columns import delete_unnecessary_columns
from src.main.processing.coding_assistant_processing.filter_incorrect_fragments import filter_incorrect_fragments
from src.main.processing.coding_assistant_processing.filter_same_fragments import filter_same_fragments
from src.main.processing.coding_assistant_processing.unify_program_experience import unify_program_experience
from src.main.task_scoring.task_scoring import unpack_tests_results


def coding_assistant_processing(path: str) -> str:
    """
    This function allows to process data for the coding-assistant project.
    The detailed description for each function can be found in the description for this function.

    Shortly, this processing contains the following steps:
    - unpack tests results and add a column with the task
    - unify program experience column
    - keep only several columns
    - filter incorrect fragments
    - keep unique fragments and add numbers of row
    """
    processing_functions = [unpack_tests_results, unify_program_experience, delete_unnecessary_columns,
                            filter_incorrect_fragments, filter_same_fragments]
    for f in processing_functions:
        path = f(path)
    return path
