# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import os

from src.main.util.consts import TASK
from src.main.util.cli_util import ICli
from src.main.util.configs import ALGO_LEVEL
from src.main.util.file_util import add_slash
from src.main.util.log_util import log_and_raise_error
from src.main.solution_space.solution_space_handler import construct_solution_graph
from src.main.solution_space.solution_space_serializer import SolutionSpaceSerializer
from src.main.solution_space.solution_space_visualizer import SolutionSpaceVisualizer
from src.main.plots.solution_graph_statistics_plots import plot_node_numbers_statistics, \
    plot_node_numbers_freq_for_each_vertex


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
        self._parser.add_argument('path', type=str, nargs=1, help=f'set path of the folder with files to construct '
                                                                  'the solution graph or path of the serialized '
                                                                  'solution graph. Note: if you want deserialize the '
                                                                  'graph, you should use param --deserialize')
        self._parser.add_argument('--level', nargs='?', const=ALGO_LEVEL.max_value(),
                                  default=ALGO_LEVEL.max_value(),
                                  help=ALGO_LEVEL.description())
        self._parser.add_argument('--task', nargs='?', const=TASK.PIES.value, default=TASK.PIES.value,
                                  help='task for the algorithm')
        self._parser.add_argument('--construct', type=self.str_to_bool, nargs='?', const=True, default=True,
                                  help='to construct graph. Note: you should use only one param from the set '
                                       '{--construct, --deserialize} in the same time')
        self._parser.add_argument('--deserialize', type=self.str_to_bool, nargs='?', const=False, default=False,
                                  help='to deserialize graph. Note: you should use only one param from the set '
                                       '{--construct, --deserialize} in the same time')
        self._parser.add_argument('--serialize', type=self.str_to_bool, nargs='?', const=False, default=False,
                                  help='to serialize graph')
        self._parser.add_argument('--viz', type=self.str_to_bool, nargs='?', const=True, default=True,
                                  help='to visualize graph')
        self._parser.add_argument('--nod_num_stat', type=self.str_to_bool, nargs='?', const=False, default=False,
                                  help='to visualize the number of nodes statistics (for each vertex and in general)')

    def __construct_graph(self) -> None:
        if self._to_construct:
            self._graph = construct_solution_graph(self._path, self._task)
            self._log.info('Graph was constructed')
        elif self._to_deserialize:
            self._graph = SolutionSpaceSerializer.deserialize(self._path)
            self._log.info('Graph was deserialized')
        else:
            log_and_raise_error('Can not create the solution graph. The params --construct and --deserialize are False',
                                self._log)

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
            log_and_raise_error(f'You can use only one param from the set (--construct, --deserialize) in the same '
                                f'time', self._log)
        self._to_construct = args.construct
        self._to_deserialize = args.deserialize
        self._to_serialize = args.serialize
        self._to_visualize = args.viz
        self._to_get_nodes_number_statistics = args.nod_num_stat
        path = args.path[0]
        if not os.path.exists(args.path[0]):
            log_and_raise_error(f'Path {path} does not exist', self._log)
        if self._to_construct:
            path = add_slash(path)
        self._path = path
        self._level = ALGO_LEVEL.get_level(args.level)
        self._task = self.get_task(args.task)

    def main(self) -> None:
        self.parse_args()

        # Todo: add others args and functions (for getting hints)
        algo_functions = [self.__construct_graph]

        for function_index in range(0, self._level.value + 1):
            algo_functions[function_index]()


if __name__ == '__main__':
    algo_cli = AlgoCli()
    algo_cli.main()
