import os
import logging
import re
import unittest

from src.main.canonicalization.canonicalization import get_code_from_tree, get_canonicalized_and_orig_form, \
    get_canonicalized_form, get_cleaned_code
from src.main.canonicalization.diffs.diff_worker import DiffWorker
from src.main.util.consts import LOGGER_TEST_FILE, LOGGER_FORMAT
from src.main.util.file_util import get_content_from_file, get_parent_folder, get_name_from_path
from src.test.canonicalization.util import run_test, DIFF_WORKER_TEST_TYPES


DST_FOLDER = 'destinations'


def get_dst_source_code(source_file: str) -> str:
    dst_path = os.path.join(get_parent_folder(source_file), DST_FOLDER, get_name_from_path(source_file))
    source = get_content_from_file(dst_path)
    return get_cleaned_code(source).rstrip('\n')


def apply_diffs(source_file: str) -> str:
    source = get_content_from_file(source_file)
    dst_source = get_content_from_file(re.sub(r'in(?=[^in]*$)', 'out', source_file))

    anon_dst_tree, orig_dst_tree = get_canonicalized_and_orig_form(dst_source, only_anon=True)
    canon_dst_tree = get_canonicalized_form(anon_dst_tree)

    diff_worker = DiffWorker(source)
    edits, tree_type = diff_worker.get_diffs(anon_dst_tree, canon_dst_tree)
    res_tree = diff_worker.apply_diffs(edits, tree_type)
    return get_code_from_tree(res_tree).rstrip('\n')


class TestDiffWorker(unittest.TestCase):
    def setUp(self) -> None:
        logging.basicConfig(filename=LOGGER_TEST_FILE, format=LOGGER_FORMAT, level=logging.INFO)

    # Find and apply all edits
    def test_diff_worker_with_all_edits(self) -> None:
        run_test(self, DIFF_WORKER_TEST_TYPES.DIFF_WORKER.value, apply_diffs,
                 additional_folder_name=DST_FOLDER,
                 to_clear_out=True)