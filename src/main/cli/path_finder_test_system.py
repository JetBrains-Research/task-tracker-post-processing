# Copyright (c) by anonymous author(s)

import sys
import logging

sys.path.append('.')
from src.main.util import consts
from src.main.cli.algo import AlgoCli
from src.main.util.consts import INT_EXPERIENCE
from src.main.solution_space.path_finder_test_system import TestSystem
from src.main.util.log_util import configure_logger, add_console_stream


log = logging.getLogger(consts.LOGGER_NAME)


class TestSystemCli(AlgoCli):

    def __init__(self):
        super().__init__()

    def main(self) -> None:
        self.parse_args()
        self.__construct_graph()

        # It's possible not to include TEST_INPUT.RATE in dict, in this case it will be found by
        # running tests on TEST_INPUT.SOURCE_CODE.
        # However, to speed up the process, one may include TEST_INPUT.RATE.
        # Todo: get ages and experiences from args?
        ages = [12, 15, 18]
        experiences = [INT_EXPERIENCE.LESS_THAN_HALF_YEAR, INT_EXPERIENCE.FROM_ONE_TO_TWO_YEARS,
                       INT_EXPERIENCE.MORE_THAN_SIX]
        test_fragments = TestSystem.generate_all_test_inputs(ages, experiences,
                                                             TestSystem.get_fragments_for_task(self._task))
        ts = TestSystem(test_fragments, task=self._task, add_same_docs=False, graph=self._graph)


if __name__ == '__main__':
    configure_logger(to_delete_previous_logs=True)
    add_console_stream(log)

    test_system_cli = TestSystemCli()
    test_system_cli.main()
