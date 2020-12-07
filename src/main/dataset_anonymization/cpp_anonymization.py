# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import subprocess

import pandas as pd

from src.main.task_scoring.task_scoring import unpack_tests_results, TESTS_RESULTS
from src.main.util.consts import LANGUAGE, FILE_SYSTEM_ITEM, EXTENSION, ISO_ENCODING, TASK_TRACKER_COLUMN, TEST_RESULT, \
    TASK
from src.main.util.file_util import remove_slash, get_parent_folder, get_all_file_system_items, task_item_condition, \
    get_name_from_path, extension_file_condition, get_content_from_file, create_file, remove_directory


class GorshochekAnonymizer:

    def __init__(self, local_gorshochek_path: str):
        self._local_gorshochek_path = remove_slash(local_gorshochek_path)
        self._input_name = 'input'
        self._data_name = 'data'
        self._out_name = f'{self._data_name}_out'
        self._input_dir = f'{local_gorshochek_path}/{self._data_name}'
        self._output_dir = f'{local_gorshochek_path}/{self._out_name}'

    def anonymize_code_fragment(self, code_fragment: str):
        """
        gorshochek works only with folders with cpp files. We create a folder with the code fragment and run gorshochek.

        Note: the default scripts/run.sh file in the gorshochek repository requires sudo access for docker running.
        We remove it for the anonymization process to avoid running sudo processes from an external process.

        After getting the result we delete the created folders.
        """
        create_file(code_fragment, f'{self._input_dir}/{self._input_name}.cpp')
        p = subprocess.Popen(['sh', f'./scripts/run.sh', self._data_name, self._out_name],
                             cwd=self._local_gorshochek_path)
        p.wait()
        return get_content_from_file(f'{self._output_dir}/{self._input_name}/transformation_1.cpp')

    def remove_directories(self):
        remove_directory(self._input_dir)
        remove_directory(self._output_dir)


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
          rename functions: true
          rename variables: true
          strategy:
              name: hash
              hash prefix: d

    You can change 'seed', 'max tokens', 'max token len' params if you want.
    """
    cpp_path = f'{remove_slash(root)}/{LANGUAGE.CPP.value}'
    output_path = f'{get_parent_folder(root)}/{output_folder_name}/{LANGUAGE.CPP.value}'

    task_dirs = get_all_file_system_items(cpp_path,
                                          item_condition=task_item_condition,
                                          item_type=FILE_SYSTEM_ITEM.SUBDIR)
    gorshochek_anonymizer = GorshochekAnonymizer(local_gorshochek_path)
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
            df[TASK_TRACKER_COLUMN.FRAGMENT.value] = \
                df[TASK_TRACKER_COLUMN.FRAGMENT.value].apply(gorshochek_anonymizer.anonymize_code_fragment)
            current_output_path = f'{output_path}/{task}/{get_name_from_path(file)}'
            create_file('', current_output_path)
            df.to_csv(current_output_path)

    gorshochek_anonymizer.remove_directories()
