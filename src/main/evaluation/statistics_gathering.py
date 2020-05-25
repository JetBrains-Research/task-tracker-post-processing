# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import logging
from typing import Optional, Tuple, List, Callable

from src.main.util import consts
from src.main.util.consts import UTF_ENCODING
from src.main.util.log_util import log_and_raise_error
from src.main.util.file_util import get_content_from_file
from src.main.evaluation.util import HINT_SIZE, HINT_STRUCTURE, HINT_TO_SOLUTION_DISTANCE, HINT_STEP, HINT_QUALITY, \
    APPLY_DIFFS_QUALITY, HINT_SOLUTION

log = logging.getLogger(consts.LOGGER_NAME)


class FragmentStatistics:
    def __init__(self, fragment_id: str, is_not_solution: bool, is_solution: bool,
                 hint_size: Optional[HINT_SIZE], hint_structure: Optional[HINT_STRUCTURE],
                 hint_to_solution_distance: Optional[HINT_TO_SOLUTION_DISTANCE], hint_step: Optional[HINT_STEP],
                 hint_quality: Optional[HINT_QUALITY], apply_diffs_quality: Optional[APPLY_DIFFS_QUALITY]):
        self._fragment_id = fragment_id
        self._hint_solution = HINT_SOLUTION.get_hint_solution(is_solution, is_not_solution)
        self._hint_size = hint_size
        self._hint_structure = hint_structure
        self._hint_to_solution_distance = hint_to_solution_distance
        self._hint_step = hint_step
        self._hint_quality = hint_quality
        self._apply_diffs_quality = apply_diffs_quality

    @property
    def fragment_id(self) -> str:
        return self._fragment_id

    @property
    def hint_solution(self) -> Optional[HINT_SOLUTION]:
        return self._hint_solution

    @property
    def hint_size(self) -> Optional[HINT_SIZE]:
        return self._hint_size

    @property
    def hint_structure(self) -> Optional[HINT_STRUCTURE]:
        return self._hint_structure

    @property
    def hint_to_solution_distance(self) -> Optional[HINT_TO_SOLUTION_DISTANCE]:
        return self._hint_to_solution_distance

    @property
    def hint_step(self) -> Optional[HINT_STEP]:
        return self._hint_step

    @property
    def hint_quality(self) -> Optional[HINT_QUALITY]:
        return self._hint_quality

    @property
    def apply_diffs_quality(self) -> Optional[APPLY_DIFFS_QUALITY]:
        return self._apply_diffs_quality


class EvaluationStatisticsHandler:
    separator = '\n'
    table_separator = '\t'
    labeled_symbol = '-'
    statistics_printer_separator = '________________________________________________'

    def __init__(self, file: str, max_number_of_fragments: int = 100):
        self._fragments = self.__parse_file_with_statistics(file, max_number_of_fragments=max_number_of_fragments)

    def __does_contain_labeled_symbol(self, items: List[str]) -> List[bool]:
        return [self.labeled_symbol in item for item in items]

    # Return (fragment_id, is_not_solution, HINT_SIZE)
    def __handle_not_solution_piece(self, not_solution_piece: str) -> Tuple[str, bool, Optional[HINT_SIZE]]:
        not_solution_piece = not_solution_piece.lstrip(self.separator).split(self.separator)
        # Todo: add into class variables
        if len(not_solution_piece) != 4:
            log_and_raise_error(f'Not solution piece in statistics has an incorrect structure', log)
        fragment_id = not_solution_piece[0]
        is_not_solution = self.labeled_symbol in not_solution_piece[1]
        return fragment_id, is_not_solution, \
               HINT_SIZE.get_hint_size(*self.__does_contain_labeled_symbol(not_solution_piece[2:]))

    # Return (is_solution, HINT_STRUCTURE, HINT_TO_SOLUTION_DISTANCE, HINT_STEP, HINT_QUALITY, APPLY_DIFFS_QUALITY)
    def __handle_solution_piece(self, solution_piece: str) -> Tuple[bool, Optional[HINT_STRUCTURE],
                                                                    Optional[HINT_TO_SOLUTION_DISTANCE],
                                                                    Optional[HINT_STEP],
                                                                    Optional[HINT_QUALITY],
                                                                    Optional[APPLY_DIFFS_QUALITY]]:
        solution_piece = solution_piece.split(self.separator * 2)
        # Todo: add into class variables
        if len(solution_piece) != 5:
            log_and_raise_error(f'Solution piece in statistics has an incorrect structure', log)

        # handle hint structure
        hint_structure_info = solution_piece[0].split(self.separator + self.table_separator)
        is_solution = self.labeled_symbol in hint_structure_info[0]
        hint_structure = HINT_STRUCTURE.get_hint_structure(*self.__does_contain_labeled_symbol(hint_structure_info[1:]))

        converters = [HINT_TO_SOLUTION_DISTANCE.get_hint_to_solution_distance,
                      HINT_STEP.get_hint_step,
                      HINT_QUALITY.get_hint_quality,
                      APPLY_DIFFS_QUALITY.get_apply_diffs_quality]
        parsed_info = []
        for index, piece in enumerate(solution_piece[1:]):
            info = piece.split(self.separator + self.table_separator)
            parsed_info.append(converters[index](*self.__does_contain_labeled_symbol(info)))
        return (is_solution, hint_structure, *parsed_info)

    def __get_statistics_from_fragment(self, fragment: str) -> FragmentStatistics:
        statistics = fragment.split(self.separator * 3)
        if len(statistics) != 2:
            log_and_raise_error(f'Statistics has an incorrect structure', log)
        fragment_id, is_not_solution, hint_size = self.__handle_not_solution_piece(statistics[0])
        is_solution, hint_structure, hint_to_solution_distance, hint_step, hint_quality, apply_diffs_quality = self.__handle_solution_piece(
            statistics[1])
        return FragmentStatistics(fragment_id, is_not_solution, is_solution, hint_size, hint_structure,
                                  hint_to_solution_distance, hint_step, hint_quality, apply_diffs_quality)

    def __parse_file_with_statistics(self, file: str, max_number_of_fragments: int = 100) -> List[FragmentStatistics]:
        statistics = get_content_from_file(file, encoding=UTF_ENCODING)
        fragments = statistics.split(self.separator * 4)
        if len(fragments) < max_number_of_fragments:
            log_and_raise_error(f'Fragments number is {len(fragments)}, but max number of fragments is '
                                f'{max_number_of_fragments}', log)
        fragments = fragments[:max_number_of_fragments]
        return list(map(self.__get_statistics_from_fragment, fragments))

    # Use HINT_SOLUTION: SOLUTION
    def __get_statistics_for_solutions_by_condition(self, good_case_condition: Callable) -> Tuple[int, int]:
        good, bad = 0, 0
        for fragment in self._fragments:
            if fragment.hint_solution == HINT_SOLUTION.SOLUTION:
                if good_case_condition(fragment):
                    good += 1
                else:
                    bad += 1
        return good, bad

    # {GOOD, NORMAL} vs {BAD}
    def __get_hint_quality_statistics(self) -> Tuple[int, int]:
        return self.__get_statistics_for_solutions_by_condition(
            lambda f: f.hint_quality == HINT_QUALITY.GOOD or f.hint_quality == HINT_QUALITY.NORMAL)

    # {CORRECT} vs {INCORRECT}
    def __get_apply_diffs_quality_statistics(self) -> Tuple[int, int]:
        return self.__get_statistics_for_solutions_by_condition(
            lambda f: f.apply_diffs_quality == APPLY_DIFFS_QUALITY.CORRECT)

    # HINT_STRUCTURE: SIMILAR
    # HINT_TO_SOLUTION_DISTANCE: APPROXIMATE
    # HINT_STEP: NORMAL
    # HINT_QUALITY: {GOOD, NORMAL}
    # vs others with HINT_SOLUTION: SOLUTION
    # Todo: rename
    def __get_approximate_structure_with_good_hint_statistics(self) -> Tuple[int, int]:
        return self.__get_statistics_for_solutions_by_condition(lambda f:
                                                                f.hint_structure == HINT_STRUCTURE.SIMILAR and
                                                                f.hint_to_solution_distance == HINT_TO_SOLUTION_DISTANCE.APPROXIMATE and
                                                                f.hint_step == HINT_STEP.NORMAL and
                                                                (f.hint_quality == HINT_QUALITY.GOOD or f.hint_quality == HINT_QUALITY.NORMAL))

    # HINT_STRUCTURE: DISSIMILAR
    # HINT_TO_SOLUTION_DISTANCE: APPROXIMATE
    # HINT_STEP: NORMAL
    # HINT_QUALITY: {GOOD, NORMAL}
    # vs others with HINT_SOLUTION: SOLUTION
    # Todo: rename
    def __get_dissimilar_structure_with_good_hint_statistics(self) -> Tuple[int, int]:
        return self.__get_statistics_for_solutions_by_condition(lambda f:
                                                                f.hint_structure == HINT_STRUCTURE.DISSIMILAR and
                                                                f.hint_to_solution_distance == HINT_TO_SOLUTION_DISTANCE.APPROXIMATE and
                                                                f.hint_step == HINT_STEP.NORMAL and
                                                                (f.hint_quality == HINT_QUALITY.GOOD or f.hint_quality == HINT_QUALITY.NORMAL))

    # HINT_STRUCTURE: SIMILAR
    # HINT_TO_SOLUTION_DISTANCE: APPROXIMATE
    # HINT_STEP: {BIG, SMALL}
    # HINT_QUALITY: {GOOD, NORMAL}
    # vs others with HINT_SOLUTION: SOLUTION
    # Todo: rename
    def __get_approximate_structure_with_different_steps_statistics(self) -> Tuple[int, int]:
        return self.__get_statistics_for_solutions_by_condition(lambda f:
                                                                f.hint_structure == HINT_STRUCTURE.SIMILAR and
                                                                f.hint_to_solution_distance == HINT_TO_SOLUTION_DISTANCE.APPROXIMATE and
                                                                (f.hint_step == HINT_STEP.BIG or f.hint_step == HINT_STEP.SMALL) and
                                                                (f.hint_quality == HINT_QUALITY.GOOD or f.hint_quality == HINT_QUALITY.NORMAL))

    # HINT_STRUCTURE: SIMILAR
    # HINT_TO_SOLUTION_DISTANCE: APPROXIMATE
    # HINT_QUALITY: {GOOD, NORMAL}
    # vs others with HINT_SOLUTION: SOLUTION
    # Todo: rename
    def __get_approximate_structure_without_steps_statistics(self) -> Tuple[int, int]:
        return self.__get_statistics_for_solutions_by_condition(lambda f:
                                                                f.hint_structure == HINT_STRUCTURE.SIMILAR and
                                                                f.hint_to_solution_distance == HINT_TO_SOLUTION_DISTANCE.APPROXIMATE and
                                                                (f.hint_quality == HINT_QUALITY.GOOD or f.hint_quality == HINT_QUALITY.NORMAL))

    # HINT_STRUCTURE: SIMILAR
    # HINT_TO_SOLUTION_DISTANCE: APPROXIMATE
    # HINT_STEP: {BIG, NORMAL}
    # HINT_QUALITY: {GOOD, NORMAL}
    # vs others with HINT_SOLUTION: SOLUTION
    # Todo: rename
    def __get_approximate_structure_with_different_big_and_normal_steps_statistics(self) -> Tuple[int, int]:
        return self.__get_statistics_for_solutions_by_condition(lambda f:
                                                                f.hint_structure == HINT_STRUCTURE.SIMILAR and
                                                                f.hint_to_solution_distance == HINT_TO_SOLUTION_DISTANCE.APPROXIMATE and
                                                                (f.hint_step == HINT_STEP.BIG or f.hint_step == HINT_STEP.NORMAL) and
                                                                (f.hint_quality == HINT_QUALITY.GOOD or f.hint_quality == HINT_QUALITY.NORMAL))

    @staticmethod
    def __get_percents(current: int, all: int) -> float:
        return round((current / all) * 100, 2)

    def __print_one_statistics(self, good: int, bad: int, comment: str) -> None:
        all = good + bad
        print(f'{comment}\n({good} examples, {bad} examples)\n'
              f'({self.__get_percents(good, all)}%, {self.__get_percents(bad, all)}%)')
        print(self.statistics_printer_separator)

    def print_statistics(self) -> None:
        good, bad = self.__get_hint_quality_statistics()
        self.__print_one_statistics(good, bad, 'Good or normal VS bad quality of a hint:')

        good, bad = self.__get_apply_diffs_quality_statistics()
        self.__print_one_statistics(good, bad, 'Correct VS incorrect diffs applying:')

        good, bad = self.__get_approximate_structure_with_good_hint_statistics()
        self.__print_one_statistics(good, bad, 'Hint structure: SIMILAR\nHint to solution distance: APPROXIMATE\n'
                                               'Hint step: NORMAL\nHint quality: {GOOD, NORMAL} VS others, which '
                                               'are the task solution')

        good, bad = self.__get_dissimilar_structure_with_good_hint_statistics()
        self.__print_one_statistics(good, bad, 'Hint structure: DISSIMILAR\nHint to solution distance: APPROXIMATE\n'
                                               'Hint step: NORMAL\nHint quality: {GOOD, NORMAL} VS others, which '
                                               'are the task solution')

        good, bad = self.__get_approximate_structure_with_different_steps_statistics()
        self.__print_one_statistics(good, bad, 'Hint structure: SIMILAR\nHint to solution distance: APPROXIMATE\n'
                                               'Hint step: {BIG, SMALL}\nHint quality: {GOOD, NORMAL} VS others, which '
                                               'are the task solution')

        good, bad = self.__get_approximate_structure_without_steps_statistics()
        self.__print_one_statistics(good, bad, 'Hint structure: SIMILAR\nHint to solution distance: APPROXIMATE\n'
                                               'Hint quality: {GOOD, NORMAL} VS others, which are the task solution')

        good, bad = self.__get_approximate_structure_with_different_big_and_normal_steps_statistics()
        self.__print_one_statistics(good, bad, 'Hint structure: SIMILAR\nHint to solution distance: APPROXIMATE\n'
                                               'Hint step: {BIG, NORMAL}\nHint quality: {GOOD, NORMAL} '
                                               'VS others, which are the task solution')
