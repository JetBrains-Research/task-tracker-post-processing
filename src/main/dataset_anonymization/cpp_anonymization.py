# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import subprocess
from typing import Optional

import pandas as pd

from src.main.task_scoring.task_scoring import unpack_tests_results, TESTS_RESULTS
from src.main.util.consts import LANGUAGE, FILE_SYSTEM_ITEM, EXTENSION, ISO_ENCODING, CODE_TRACKER_COLUMN, TEST_RESULT, \
    TASK
from src.main.util.file_util import remove_slash, get_parent_folder, get_all_file_system_items, task_item_condition, \
    get_name_from_path, extension_file_condition, get_content_from_file, create_file, remove_directory


def __anonymize_code_fragment(code_fragment: str, local_gorshochek_path: str) -> Optional[str]:
    """
    gorshochek works only with folders with cpp files. We create a folder with the code fragment and run gorshochek.

    Note: the default scripts/run.sh file in the gorshochek repository requires sudo access for docker running.
    We remove it for the anonymization process to avoid running sudo processes from an external process.

    After getting the result we delete the crested folders.
    """
    print(f'Start handling the code fragment:\n{code_fragment}\n\n')
    input_name = 'input'
    data_name = 'data'
    out_name = f'{data_name}_out'
    local_gorshochek_path = remove_slash(local_gorshochek_path)
    input_dir = f'{local_gorshochek_path}/{data_name}'
    create_file(code_fragment, f'{input_dir}/{input_name}.cpp')
    output_dir = f'{local_gorshochek_path}/{out_name}'
    p = subprocess.Popen(['sh', f'./scripts/run.sh', data_name, out_name], cwd=local_gorshochek_path)
    p.wait()
    print('Try to get the result')
    anonymized_code = get_content_from_file(f'{output_dir}/{input_name}/transformation_1.cpp')
    remove_directory(input_dir)
    remove_directory(output_dir)
    return anonymized_code


def is_incorrect_fragment(tests_results: str) -> bool:
    return TEST_RESULT.INCORRECT_CODE.value in unpack_tests_results(tests_results, TASK.tasks())


def anonymize_cpp_code(root: str, local_gorshochek_path: str, output_folder_name: str = 'anonymizerResult') -> None:
    """
    We use gorshochek library: https://github.com/JetBrains-Research/gorshochek
    You need to clone the repo and build a docker image (see gorshochek README).

    Note: you need to change the config.yaml file before building the docker image:

    n transformations: 1
    transformations:
      - remove comments:
          p: 1.0
      - rename entities:
          p: 1
          seed: 9
          max tokens: 2
          max token len: 3
          rename functions: true
          rename variables: true
          test: false

    You can change 'seed', 'max tokens', 'max token len' params if you want.
    """
    cpp_path = f'{remove_slash(root)}/{LANGUAGE.CPP.value}'
    output_path = f'{get_parent_folder(root)}/{output_folder_name}/{LANGUAGE.CPP.value}'

    task_dirs = get_all_file_system_items(cpp_path,
                                          item_condition=task_item_condition,
                                          item_type=FILE_SYSTEM_ITEM.SUBDIR)
    for task_dir in task_dirs:
        task = get_name_from_path(task_dir, with_extension=False)
        print(f'Start handling the task {task}')
        files = get_all_file_system_items(task_dir,
                                          item_condition=extension_file_condition(EXTENSION.CSV))
        for file in files:
            print(f'Start handling the file {file}')
            df = pd.read_csv(file, encoding=ISO_ENCODING)
            # Delete incorrect fragments
            df = df[df.apply(lambda row: not is_incorrect_fragment(row[TESTS_RESULTS]), axis=1)]
            df[CODE_TRACKER_COLUMN.FRAGMENT.value] = \
                df[CODE_TRACKER_COLUMN.FRAGMENT.value].apply(lambda code: __anonymize_code_fragment(code, local_gorshochek_path))
            current_output_path = f'{output_path}/{task}/{get_name_from_path(file)}'
            create_file('', current_output_path)
            df.to_csv(current_output_path)
