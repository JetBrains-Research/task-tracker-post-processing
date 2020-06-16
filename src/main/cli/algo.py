# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import sys
import logging

sys.path.append('.')
from src.main.util import consts
from src.main.cli.util import ICli
from src.main.util.consts import TASK
from src.main.cli.configs import ALGO_LEVEL, ALGO_PARAMS
from src.main.solution_space.solution_space_handler import construct_solution_graph
from src.main.solution_space.solution_space_serializer import SolutionSpaceSerializer
from src.main.solution_space.solution_space_visualizer import SolutionSpaceVisualizer
from src.main.util.log_util import log_and_raise_error, configure_logger, add_console_stream
from src.main.plots.solution_graph_statistics_plots import plot_node_numbers_statistics, \
    plot_node_numbers_freq_for_each_vertex

log = logging.getLogger(consts.LOGGER_NAME)


class AlgoCli(ICli):

    def __init__(self):
        super().__init__()
        self._path = None
        self._level = None
        self._to_construct = True
        self._to_deserialize = False
        self._to_serialize = False
        self._to_visualize = True
        self._task = None
        self._graph = None
        self._to_get_nodes_number_statistics = False

    def configure_args(self) -> None:
        note_message = f'Note: if you want to deserialize the graph, you should use param ' \
                       f'{ALGO_PARAMS.DESERIALIZE.value}, default action is construction.'
        self._parser.add_argument(ALGO_PARAMS.PATH.value, type=str, nargs=1,
                                  help=f'set path of the folder with files to construct the '
                                       f'solution graph or path of the serialized solution '
                                       f'graph to deserialize the solution graph. '
                                       + note_message)
        self._parser.add_argument(ALGO_PARAMS.LEVEL.value, nargs='?', const=ALGO_LEVEL.max_value(),
                                  default=ALGO_LEVEL.max_value(),
                                  help=ALGO_LEVEL.description())
        self._parser.add_argument(ALGO_PARAMS.TASK.value, nargs='?', const=TASK.PIES.value, default=TASK.PIES.value,
                                  help='task for the algorithm')
        note_message = f'Note: you should use only one param from the set {ALGO_PARAMS.CONSTRUCT.value}, ' \
                       f'{ALGO_PARAMS.DESERIALIZE.value} in the same time'
        self._parser.add_argument(ALGO_PARAMS.CONSTRUCT.value, type=self.str_to_bool, nargs='?', const=True,
                                  default=False,
                                  help='to construct graph. ' + note_message)
        self._parser.add_argument(ALGO_PARAMS.DESERIALIZE.value, type=self.str_to_bool, nargs='?', const=True,
                                  default=False,
                                  help='to deserialize graph. ' + note_message)
        self._parser.add_argument(ALGO_PARAMS.SERIALIZE.value, type=self.str_to_bool, nargs='?', const=True,
                                  default=False,
                                  help='to serialize graph')
        self._parser.add_argument(ALGO_PARAMS.VISUALIZE.value, type=self.str_to_bool, nargs='?', const=True,
                                  default=True,
                                  help='to visualize graph')
        self._parser.add_argument(ALGO_PARAMS.NOD_NUM_STAT.value, type=self.str_to_bool, nargs='?', const=True,
                                  default=False,
                                  help='to visualize the number of nodes statistics (for each vertex and in general)')

    def __construct_graph(self) -> None:
        if self._to_construct:
            self._graph = construct_solution_graph(self._path, self._task)
            self._log.info('Graph was constructed')
        elif self._to_deserialize:
            self._graph = SolutionSpaceSerializer.deserialize(self._path)
            self._log.info('Graph was deserialized')

        if self._to_serialize:
            path = SolutionSpaceSerializer.serialize(self._graph)
            self._log.info(f'Serialized graph path: {path}')
            print(f'Serialized graph path: {path}')

        if self._to_visualize:
            gv = SolutionSpaceVisualizer(self._graph)
            graph_visualization_path = gv.visualize_graph(name_prefix=f'{self._task.value}')
            self._log.info(f'Graph visualization path: {graph_visualization_path}')

        if self._to_get_nodes_number_statistics:
            plot_node_numbers_statistics(self._graph)
            plot_node_numbers_freq_for_each_vertex(self._graph)

    def parse_args(self) -> None:
        args = self._parser.parse_args()
        if args.construct and args.deserialize:
            log_and_raise_error(f'You can use only one param from the set ({ALGO_PARAMS.CONSTRUCT.value}, '
                                f'{ALGO_PARAMS.DESERIALIZE.value}) in the same '
                                f'time', self._log)
        # Todo: find a better way to use construct and deserialize args
        if not args.deserialize:
            self._to_construct = True
        else:
            self._to_construct = args.construct
        self._to_deserialize = args.deserialize
        self._to_serialize = args.serialize
        self._to_visualize = args.viz
        self._to_get_nodes_number_statistics = args.nod_num_stat
        # If self._to_construct is True then add slash else don't
        self._path = self.handle_path(args.path[0], self._to_construct)
        self._level = self.str_to_algo_level(args.level)
        self._task = self.str_to_task(args.task)

    # Todo: implement it
    def __get_hint(self) -> None:
        pass

    def main(self) -> None:
        self.parse_args()

        # Todo: add others args and functions (for getting hints)
        algo_functions = [self.__construct_graph, self.__get_hint]

        for function_index in range(0, self._level.value + 1):
            algo_functions[function_index]()


if __name__ == '__main__':
    configure_logger(to_delete_previous_logs=True)
    add_console_stream(log)

    algo_cli = AlgoCli()
    algo_cli.main()
