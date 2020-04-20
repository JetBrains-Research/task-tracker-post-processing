import itertools

from src.main.canonicalization.consts import TREE_TYPE
from src.main.solution_space.code import Code
from src.main.solution_space.data_classes import CodeInfo, User
from src.main.solution_space.solution_graph import SolutionGraph
from src.main.util.consts import TASK, LOGGER_NAME
from src.test.solution_space.solution_graph.util import create_code_from_source
from src.test.test_util import LoggedTest
from src.main.canonicalization.canonicalization import get_trees, get_code_from_tree, are_asts_equal, List, Tuple, \
    logging

log = logging.getLogger(LOGGER_NAME)

# Fragments with the same canon tree for the first vertex:
fragment_1 = "a = 5\n" \
             "if a < 6:\n" \
             "    print(a)"

fragment_2 = "five = 5\n" \
             "if 6 > five:\n" \
             "    print(5)"

fragment_3 = "c = 4 + 1\n" \
             "if c < (7 - 1):\n" \
             "    print(4+1)"

vertex_fragments_1 = [fragment_1, fragment_2, fragment_3]


# Fragments with the same canon tree for the second vertex:
fragment_4 = "a = int(input())\n" \
             "c = 5\n" \
             "print((a + b)*6)"

fragment_5 = "a = int(input())\n" \
             "c = 1 + 1 + 1 + 1 + 1\n" \
             "print(6*(a + b))"

vertex_fragments_2 = [fragment_4, fragment_5]

# Fragment for the third vertex:
fragment_6 = "a = int(input())\n" \
             "b = int(input())"

vertex_fragments_3 = [fragment_6]


def get_code_info_chain(sources: List[str]) -> List[Tuple[Code, CodeInfo]]:
    user = User()
    return [(create_code_from_source(s), CodeInfo(user)) for s in sources]




class TestDistBetweenVertices(LoggedTest):

    def test_having_same_canon_tree(self):
        for fragments in [vertex_fragments_1, vertex_fragments_2]:
            canon_trees = (get_trees(f, {TREE_TYPE.CANON})[0] for f in fragments)
            for canon_tree_1, canon_tree_2 in itertools.product(canon_trees, repeat=2):
                log.info(f'canon_tree_1:\n{get_code_from_tree(canon_tree_1)}\ncanon_tree_2:\n{get_code_from_tree(canon_tree_2)}')
                self.assertTrue(are_asts_equal(canon_tree_1, canon_tree_2))

    def test_consequent_dist_updating(self):
        sg = SolutionGraph(TASK.PIES)
        code_info_chain_1 = get_code_info_chain([fragment_1, fragment_4, fragment_6])
        # code_info_chain_2 = get_code_info_chain([fragment_2, fragment_5])
        # code_info_chain_3 = get_code_info_chain([fragment_3, fragment_6])
        sg.add_code_info_chain(code_info_chain_1)
        # sg.add_code_info_chain(code_info_chain_2)
        # sg.add_code_info_chain(code_info_chain_3)






