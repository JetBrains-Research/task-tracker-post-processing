import ast
import logging
import re
import timeit
from datetime import datetime
from enum import Enum
from functools import partial
from typing import Tuple, Dict, Any, List

from src.main.canonicalization.canonicalization import get_canon_tree_from_anon_tree, get_imports, are_asts_equal, \
    get_code_from_tree
from src.main.solution_space.consts import TEST_INPUT
from src.main.solution_space.data_classes import Profile
from src.main.solution_space.hint import HintHandler
from src.main.solution_space.measured_tree.measured_tree_v_6 import MeasuredTreeV6
from src.main.solution_space.measured_tree.measured_tree_v_7 import MeasuredTreeV7
from src.main.solution_space.path_finder.path_finver_v_5 import PathFinderV5
from src.main.solution_space.serialized_code import AnonTree
from src.main.util.consts import LOGGER_NAME, UTF_ENCODING, TEST_RESULT
from src.main.solution_space.solution_graph import SolutionGraph
from src.main.solution_space.path_finder_test_system import TestSystem
from src.main.solution_space.evaluation.pseudo_solutions_sampling import sample_n_correct_test_inputs
from src.main.util.file_util import create_file, get_content_from_file

log = logging.getLogger(LOGGER_NAME)


class Evaluation:
    def __init__(self, graph: SolutionGraph,
                 path_to_fragments: str = '/home/elena/workspaces/python/codetracker-data/data/codetracker-dataset/row_data/python_pies_pseudo_solutions'):
        self._graph = graph
        self._language = graph.language
        self._task = graph.task
        self._path_to_fragments = path_to_fragments
        self._hint_handler = HintHandler(graph)
        self._path_finder = PathFinderV5(graph, MeasuredTreeV7)

    def create_user_trees(self, test_input: Dict[TEST_INPUT, Any]) -> Tuple[AnonTree, ast.AST]:
        profile = Profile(test_input[TEST_INPUT.AGE], test_input[TEST_INPUT.INT_EXPERIENCE])
        # If rate is None, it's okay, it will be found further
        rate = test_input.get(TEST_INPUT.RATE)
        user_trees = self._hint_handler.create_user_trees(test_input[TEST_INPUT.SOURCE_CODE], profile, rate)
        # Put found rate into test_input
        test_input[TEST_INPUT.RATE] = user_trees[0].rate
        return user_trees

    def evaluate(self, test_inputs_number: int) -> None:
        test_inputs = sample_n_correct_test_inputs(self._path_to_fragments, test_inputs_number)
        test_system = TestSystem(test_inputs=test_inputs, graph=self._graph, to_visualize_graph=False)

    def evaluate_time(self, test_inputs_number: int, repeat: int = 5) -> List[float]:
        test_inputs = sample_n_correct_test_inputs(self._path_to_fragments, test_inputs_number)
        results = []
        sum = 0
        for i, t_i in enumerate(test_inputs):
            print(f'Run {i} test_input')
            log.info(f'Run {i} test_input')

            anon_tree, canon_tree = self.create_user_trees(t_i)


            def to_time():
                self._path_finder.find_next_anon_tree(anon_tree, canon_tree)

            # test_items = [anon_tree, canon_tree]
            time = min(timeit.Timer(partial(to_time)).repeat(1, repeat)) / repeat
            print(f'time: {time}')
            log.info(f'time: {time}')
            results.append((time, anon_tree.nodes_number))
            sum += time
        print(results)
        print(sum)
        log.info(results)
        log.info(sum)

        return results



    def does_follow_to_full_solution(self, test_inputs_number: int) -> List[Tuple[bool, int]]:
        test_inputs = sample_n_correct_test_inputs(self._path_to_fragments, test_inputs_number)
        results = []
        for i, t_i in enumerate(test_inputs):
            print(f'Run {i}/{len(test_inputs)} test input, len: {len(t_i[TEST_INPUT.SOURCE_CODE])}')
            log.info(f'Run {i}/{len(test_inputs)} test input')
            anon_tree, canon_tree = self.create_user_trees(t_i)
            anon_trees = [anon_tree.tree]
            steps_n = 0
            get_same_tree = False
            while anon_tree.rate != TEST_RESULT.FULL_SOLUTION.value and not get_same_tree:
                log.info(f'step: {steps_n}, anon tree:\n {get_code_from_tree(anon_tree.tree)}')
                print(f'step: {steps_n}, anon tree:\n {get_code_from_tree(anon_tree.tree)}')

                anon_tree = self._path_finder.find_next_anon_tree(anon_tree, canon_tree, f'test_result_{i}_step_{steps_n}')
                canon_tree = get_canon_tree_from_anon_tree(anon_tree.tree, get_imports(anon_tree.tree))
                steps_n += 1
                for i, prev_anon_tree in enumerate(anon_trees):
                    print(f'{i} ', end='')
                    if are_asts_equal(anon_tree.tree, prev_anon_tree):
                        print(f'Get the same tree, step {steps_n}')
                        log.info(f'Get the same tree, step {steps_n}')
                        get_same_tree = True
                        break
                print('\n')
                anon_trees.append(anon_tree.tree)
            results += [(get_same_tree, steps_n)]
        print(f'results: {results}')
        log.info(f'results: {results}')

        return results



# file = '/home/elena/workspaces/python/codetracker-data/src/resources/evaluation/brackets_evaluation_file_alyona.txt'
# content = ''
# n = 100
# eval_fragment = 'не решение:\n' \
#                 '\t\tподсказка маленькая\n' \
#                 '\t\tподсказка большая\n\n\n' \
#                 'решение:\n' \
#                 '\t\tструктура подсказки похожа\n' \
#                 '\t\tструктура подсказки непохожа\n\n' \
#                 '\t\tподсказка приблизила к решению\n' \
#                 '\t\tподсказка выдала то же дерево\n' \
#                 '\t\tподсказка отдалила от решения\n' \
#                 '\t\tнепонятно, отдалила или приблизила\n\n' \
#                 '\t\tшаг подсказки ок\n' \
#                 '\t\tшаг подсказки большой\n' \
#                 '\t\tшаг подсказки маленький\n\n' \
#                 '\t\tподсказка хорошая\n' \
#                 '\t\tподсказка нормальная\n' \
#                 '\t\tподсказка плохая\n\n' \
#                 '\t\tдиффы корректно\n' \
#                 '\t\tдиффы некорректно\n\n\n\n\n'
#
# for i in range (n):
#     content += f'{i}.\n{eval_fragment}'
#
# create_file(content, file)

# data = [199, 191, 201, 154, 56, 183, 133, 161, 145, 65, 218, 157, 75, 24, 25, 111, 175, 88, 162, 174, 36, 71, 156, 163, 108, 188, 17, 192, 14, 142, 147, 112, 204, 128, 225, 1, 180, 165, 62, 190, 70, 78, 238, 79, 241, 124, 248, 55, 10, 146]
#
# results = [(True, 6), (False, 18), (True, 4), (False, 6), (False, 3), (False, 12), (True, 2), (False, 11), (True, 2), (False, 5), (False, 14), (True, 5), (False, 2), (False, 30), (False, 9), (False, 10), (False, 2), (False, 10), (False, 10), (False, 3), (True, 2), (False, 2), (True, 6), (False, 9), (False, 18), (False, 5), (False, 9), (False, 18), (False, 10), (True, 5), (False, 1), (True, 6), (True, 3), (True, 5), (False, 23), (False, 10), (False, 6), (False, 9), (False, 4), (False, 18), (False, 5), (False, 18), (False, 7), (False, 28), (False, 4), (True, 7), (False, 16), (False, 3), (False, 17), (True, 2)]
# true_n = 0
# false_n = 0
# for r in results:
#     if r[0]:
#         true_n += 1
#     else:
#         false_n += 1
#
# print(true_n, false_n)


# 175, 7, 134, 10, 252, 61, 195, 35, 67, 56, 27, 17, 70, 4, 138, 22, 101, 114, 40, 185, 63, 11, 16, 177, 212, 164, 220, 122, 94, 210, 68, 169, 117, 198, 60, 250, 52, 184, 232, 32, 73, 91, 173, 237, 87, 23, 136, 55, 130, 43,

# brackets
# [(2.2446834091999337, 265), (32.37266852180037, 12), (26.422131756599992, 127), (15.818714606799768, 1), (13.21218440119992, 91), (39.20667226820078, 127), (20.91681741499924, 128), (1.980590503998974, 308), (25.33771003879956, 145), (35.0178002066008, 127), (1.8488692640006774, 92), (26.23065755080024, 57), (30.147139358799905, 128), (15.317192122800042, 10), (1.8114029554009903, 106), (23.5582664734, 74), (19.79892306799884, 163), (24.792767097998876, 54), (2.1026807816000654, 192), (22.161590150200936, 48), (34.813720659799586, 127), (20.563944381001058, 28), (21.572148608000134, 57), (31.618768473601087, 60), (2.000664432799385, 157), (2.026506419799989, 125), (1.781053208000958, 25), (1.7633122042010654, 35), (1.7483179314003792, 75), (1.8944734785996844, 125), (35.18962884120119, 128), (14.334679242600396, 236), (2.0295427285993357, 71), (1.7640716470006736, 42), (26.09431947080011, 110), (42.3793376652, 84), (40.98924379240052, 127), (29.856477569199342, 42), (29.625427107399446, 51), (2.1600318634009454, 158), (13.942360130399175, 221), (2.1141075640000055, 71), (2.351955221600656, 265), (2.240589780999289, 69), (2.2062735952000367, 27), (25.612672973200098, 12), (2.136639400399872, 94), (35.03495681960048, 127), (26.870468913399964, 131), (30.845985094200294, 88)]
# 867.8611411692051

# [(1.6342011015993194, 75), (1.6044162990001496, 73), (22.52762063800037, 80), (1.8908026587989297, 50), (1.8874800685996889, 79), (1.911674762000621, 80), (1.687197669199668, 77), (16.345049732799815, 60), (20.610693362000166, 64), (21.384703507400992, 46), (21.379400575399632, 53), (27.091077050000603, 68), (1.732023281599686, 111), (11.397843220199865, 6), (1.9397867774008772, 51), (24.82018507920002, 24), (15.636039265600266, 57), (25.433936122601153, 81), (1.8094179548003013, 77), (19.18236638160015, 49), (20.086689646399464, 64), (23.425665234800544, 76), (46.68457634139922, 73), (45.57886709680024, 75), (1.6300997772006667, 13), (21.55124598659895, 69), (18.285423266798897, 40), (19.920539543399354, 48), (2.749115185000119, 64), (26.660726910000086, 49), (96.20043145039963, 70), (28.34016713799938, 78), (26.581647802999942, 84), (24.032321016601053, 43), (1.8406578481997713, 53), (24.046523324601004, 72), (18.35136652899964, 53), (17.188811461400473, 22), (17.816754010599105, 48), (24.296579641000427, 50), (3.674820141000964, 37), (18.94360179780051, 90), (1.7341964617997292, 49), (1.7022556494004675, 65), (1.8198482491992762, 71), (1.8018678047999857, 76), (22.675888812800984, 89), (1.7321337161993142, 78), (22.795567149599083, 98), (17.830238338599155, 33)]
# 841.8845428401996