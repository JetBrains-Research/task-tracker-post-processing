import sys

sys.path.append('.')

from src.main.canonicalization.consts import TREE_TYPE
from src.main.canonicalization.canonicalization import get_trees
from src.main.canonicalization.diffs.gumtree_diff_handler import GumTreeDiffHandler


src_source = 'a = 5'
dst_source = 'a = 6'
src_anon, = get_trees(src_source, {TREE_TYPE.ANON})
dst_anon, = get_trees(dst_source, {TREE_TYPE.ANON})
GumTreeDiffHandler.create_tmp_files_and_run_gumtree(src_anon, dst_anon)
