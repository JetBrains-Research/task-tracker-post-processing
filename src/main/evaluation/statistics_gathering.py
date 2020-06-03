# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import re
import logging
from typing import Optional, Tuple, List, Callable

from src.main.util import consts
from src.main.util.consts import UTF_ENCODING
from src.main.util.log_util import log_and_raise_error
from src.main.util.file_util import get_content_from_file
from src.main.evaluation.util import HINT_SIZE, HINT_STRUCTURE, HINT_TO_SOLUTION_DISTANCE, HINT_STEP, HINT_QUALITY, \
    QUALITY_AFTER_DIFFS_APPLIED, HINT_SOLUTION

log = logging.getLogger(consts.LOGGER_NAME)


class FragmentStatistics:
    def __init__(self, fragment_id: str, is_not_solution: bool, is_solution: bool,
                 hint_size: Optional[HINT_SIZE], hint_structure: Optional[HINT_STRUCTURE],
                 hint_to_solution_distance: Optional[HINT_TO_SOLUTION_DISTANCE], hint_step: Optional[HINT_STEP],
                 hint_quality: Optional[HINT_QUALITY], apply_diffs_quality: Optional[QUALITY_AFTER_DIFFS_APPLIED]):
        log.info(f'Start creating FragmentStatistics for the fragment with id {fragment_id}')
        self._fragment_id = fragment_id
        self._hint_solution = HINT_SOLUTION.get_hint_solution(is_solution, is_not_solution)
        self._hint_size = hint_size
        self._hint_structure = hint_structure
        self._hint_to_solution_distance = hint_to_solution_distance
        self._hint_step = hint_step
        self._hint_quality = hint_quality
        self._apply_diffs_quality = apply_diffs_quality
        log.info(f'Finish creating FragmentStatistics for the fragment with id {fragment_id}')

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
    def apply_diffs_quality(self) -> Optional[QUALITY_AFTER_DIFFS_APPLIED]:
        return self._apply_diffs_quality


class EvaluationStatisticsHandler:
    separator = '\n'
    table_separator = '\t'
    labeled_symbol = '-'
    statistics_printer_separator = '________________________________________________'
    number_of_lines_for_not_solution_piece_part = 4
    number_of_categories_for_solution_piece_part = 5

    # The file must have the following structure:
    # fragment_id
    # IS NOT SOLUTION:
    # \t\t{HINT_SIZE values}
    # \n\n
    # IS SOLUTION:
    # \t\t{HINT_STRUCTURE values}
    # \n\n
    # \t\t{HINT_TO_SOLUTION_DISTANCE values}
    # \n\n
    # \t\t{HINT_STEP values}
    # \n\n
    # \t\t{HINT_QUALITY values}
    # \n\n
    # \t\t{QUALITY_AFTER_DIFFS_APPLIED values}
    # \n\n
    #
    # Note: each category must have labeled_symbol to label the necessary option
    # (including IS NOT SOLUTION and IS SOLUTION)
    # Each value from {} must be on the new line
    def __init__(self, file: str, max_number_of_fragments: int = 100):
        self._fragments = self.__parse_file_with_statistics(file, max_number_of_fragments=max_number_of_fragments)

    @classmethod
    def __does_contain_labeled_symbol(cls, items: List[str]) -> List[bool]:
        return [cls.labeled_symbol in item for item in items]

    # Return (fragment_id, is_not_solution, HINT_SIZE)
    def __handle_not_solution_piece(self, not_solution_piece: str) -> Tuple[str, bool, Optional[HINT_SIZE]]:
        log.info(f'Start handling not solution piece of statistics')
        not_solution_piece = not_solution_piece.lstrip(self.separator).split(self.separator)
        if len(not_solution_piece) != self.number_of_lines_for_not_solution_piece_part:
            log_and_raise_error(f'Not solution piece in statistics has an incorrect structure', log)
        fragment_id = not_solution_piece[0].rstrip('.')
        is_not_solution = self.labeled_symbol in not_solution_piece[1]
        return fragment_id, is_not_solution, \
               HINT_SIZE.get_hint_size(*self.__does_contain_labeled_symbol(not_solution_piece[2:]))

    # Return (is_solution, HINT_STRUCTURE, HINT_TO_SOLUTION_DISTANCE, HINT_STEP, HINT_QUALITY, APPLY_DIFFS_QUALITY)
    def __handle_solution_piece(self, solution_piece: str) -> Tuple[bool, Optional[HINT_STRUCTURE],
                                                                    Optional[HINT_TO_SOLUTION_DISTANCE],
                                                                    Optional[HINT_STEP],
                                                                    Optional[HINT_QUALITY],
                                                                    Optional[QUALITY_AFTER_DIFFS_APPLIED]]:
        log.info(f'Start handling solution piece of statistics')
        solution_info, statistics_info = solution_piece.split(self.separator, 1)
        statistics_info = statistics_info.split(self.separator * 2)
        if len(statistics_info) != self.number_of_categories_for_solution_piece_part:
            log_and_raise_error(f'Solution piece in statistics has an incorrect structure', log)

        is_solution = self.labeled_symbol in solution_info
        converters = [HINT_STRUCTURE.get_hint_structure,
                      HINT_TO_SOLUTION_DISTANCE.get_hint_to_solution_distance,
                      HINT_STEP.get_hint_step,
                      HINT_QUALITY.get_hint_quality,
                      QUALITY_AFTER_DIFFS_APPLIED.get_apply_diffs_quality]
        parsed_info = []
        for index, piece in enumerate(statistics_info):
            info = piece.split(self.separator + self.table_separator)
            parsed_info.append(converters[index](*self.__does_contain_labeled_symbol(info)))
        return (is_solution, *parsed_info)

    def __get_statistics_from_fragment(self, fragment: str) -> FragmentStatistics:
        log.info(f'Start parsing the fragment\n{fragment}')
        statistics = fragment.split(self.separator * 3)
        if len(statistics) != 2:
            log_and_raise_error(f'The fragment has an incorrect structure', log)
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

    def __get_statistics_for_solutions_by_condition(self, good_case_condition: Callable,
                                                    hint_solution_type: HINT_SOLUTION = HINT_SOLUTION.SOLUTION) -> \
    Tuple[int, int]:
        solutions = list(filter(lambda f: f.hint_solution == hint_solution_type, self._fragments))
        good_solutions = list(filter(good_case_condition, solutions))
        return len(good_solutions), len(solutions) - len(good_solutions)

    def __get_hint_quality_statistics(self) -> Tuple[int, int]:
        """
            HINT_QUALITY: {GOOD, NORMAL} vs HINT_QUALITY: {BAD}
        """
        return self.__get_statistics_for_solutions_by_condition(
            lambda f: f.hint_quality == HINT_QUALITY.GOOD or f.hint_quality == HINT_QUALITY.NORMAL)

    def __get_apply_diffs_quality_statistics(self) -> Tuple[int, int]:
        """
            QUALITY_AFTER_DIFFS_APPLIED: {CORRECT} vs QUALITY_AFTER_DIFFS_APPLIED: {INCORRECT}
        """
        return self.__get_statistics_for_solutions_by_condition(
            lambda f: f.apply_diffs_quality == QUALITY_AFTER_DIFFS_APPLIED.CORRECT)

    # Todo: rename
    def __get_approximate_structure_with_good_hint_statistics(self) -> Tuple[int, int]:
        """
            HINT_STRUCTURE: SIMILAR
            HINT_TO_SOLUTION_DISTANCE: CLOSE
            HINT_STEP: NORMAL
            HINT_QUALITY: {GOOD, NORMAL}
            vs others with HINT_SOLUTION: SOLUTION
        """
        return self.__get_statistics_for_solutions_by_condition(lambda f:
                                                                f.hint_structure == HINT_STRUCTURE.SIMILAR and
                                                                f.hint_to_solution_distance == HINT_TO_SOLUTION_DISTANCE.CLOSE and
                                                                f.hint_step == HINT_STEP.NORMAL and
                                                                (f.hint_quality == HINT_QUALITY.GOOD or f.hint_quality == HINT_QUALITY.NORMAL))

    # Todo: rename
    def __get_dissimilar_structure_with_good_hint_statistics(self) -> Tuple[int, int]:
        """
            HINT_STRUCTURE: DISSIMILAR
            HINT_TO_SOLUTION_DISTANCE: CLOSE
            HINT_STEP: NORMAL
            HINT_QUALITY: {GOOD, NORMAL}
            vs others with HINT_SOLUTION: SOLUTION
        """
        return self.__get_statistics_for_solutions_by_condition(lambda f:
                                                                f.hint_structure == HINT_STRUCTURE.DISSIMILAR and
                                                                f.hint_to_solution_distance == HINT_TO_SOLUTION_DISTANCE.CLOSE and
                                                                f.hint_step == HINT_STEP.NORMAL and
                                                                (f.hint_quality == HINT_QUALITY.GOOD or f.hint_quality == HINT_QUALITY.NORMAL))

    # Todo: rename
    def __get_approximate_structure_with_different_steps_statistics(self) -> Tuple[int, int]:
        """
            HINT_STRUCTURE: SIMILAR
            HINT_TO_SOLUTION_DISTANCE: CLOSE
            HINT_STEP: {BIG, SMALL}
            HINT_QUALITY: {GOOD, NORMAL}
            vs others with HINT_SOLUTION: SOLUTION
        """
        return self.__get_statistics_for_solutions_by_condition(lambda f:
                                                                f.hint_structure == HINT_STRUCTURE.SIMILAR and
                                                                f.hint_to_solution_distance == HINT_TO_SOLUTION_DISTANCE.CLOSE and
                                                                (f.hint_step == HINT_STEP.BIG or f.hint_step == HINT_STEP.SMALL) and
                                                                (f.hint_quality == HINT_QUALITY.GOOD or f.hint_quality == HINT_QUALITY.NORMAL))

    # Todo: rename
    def __get_approximate_structure_without_steps_statistics(self) -> Tuple[int, int]:
        """
            HINT_STRUCTURE: SIMILAR
            HINT_TO_SOLUTION_DISTANCE: CLOSE
            HINT_QUALITY: {GOOD, NORMAL}
            vs others with HINT_SOLUTION: SOLUTION
        """
        return self.__get_statistics_for_solutions_by_condition(lambda f:
                                                                f.hint_structure == HINT_STRUCTURE.SIMILAR and
                                                                f.hint_to_solution_distance == HINT_TO_SOLUTION_DISTANCE.CLOSE and
                                                                (f.hint_quality == HINT_QUALITY.GOOD or f.hint_quality == HINT_QUALITY.NORMAL))

    # Todo: rename
    def __get_approximate_structure_with_different_big_and_normal_steps_statistics(self) -> Tuple[int, int]:
        """
            HINT_STRUCTURE: SIMILAR
            HINT_TO_SOLUTION_DISTANCE: CLOSE
            HINT_STEP: {BIG, NORMAL}
            HINT_QUALITY: {GOOD, NORMAL}
            vs others with HINT_SOLUTION: SOLUTION
        """
        return self.__get_statistics_for_solutions_by_condition(lambda f:
                                                                f.hint_structure == HINT_STRUCTURE.SIMILAR and
                                                                f.hint_to_solution_distance == HINT_TO_SOLUTION_DISTANCE.CLOSE and
                                                                (f.hint_step == HINT_STEP.BIG or f.hint_step == HINT_STEP.NORMAL) and
                                                                (f.hint_quality == HINT_QUALITY.GOOD or f.hint_quality == HINT_QUALITY.NORMAL))

    @staticmethod
    def __get_readable_percents(current: int, all: int) -> float:
        return round((current / all) * 100, 2)

    @staticmethod
    def __get_readable_title(title: str) -> str:
        return re.sub(' +', ' ', title.strip('\n'))

    def print_statistics(self) -> None:
        methods_for_print = [self.__get_hint_quality_statistics,
                             self.__get_apply_diffs_quality_statistics,
                             self.__get_approximate_structure_with_good_hint_statistics,
                             self.__get_dissimilar_structure_with_good_hint_statistics,
                             self.__get_approximate_structure_with_different_steps_statistics,
                             self.__get_approximate_structure_without_steps_statistics,
                             self.__get_approximate_structure_with_different_big_and_normal_steps_statistics]

        for m in methods_for_print:
            good, bad = m()
            count = good + bad
            print(f'{self.__get_readable_title(m.__doc__)}\n({good} examples, {bad} examples)\n'
                  f'({self.__get_readable_percents(good, count)}%, {self.__get_readable_percents(bad, count)}%)')
            print(self.statistics_printer_separator)

