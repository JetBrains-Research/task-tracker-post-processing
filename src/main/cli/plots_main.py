# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import os
import argparse

from src.main.util.cli_util import ICli
from src.main.util.consts import EXTENSION
from src.main.util.configs import PLOT_TYPE
from src.main.plots.util.consts import STATISTICS_KEY, CHART_TYPE
from src.main.plots.tasks_statistics_plots import plot_tasks_statistics
from src.main.plots.profile_statistics_plots import plot_profile_statistics
from src.main.statistics_gathering.statistics_gathering import get_profile_statistics


class PlotsCli(ICli):

    def __init__(self):
        super().__init__()
        self._path = None
        self._plot_type = None
        self._type_dstr = None
        self._chart_type = None
        self._to_union_rare = False
        self._auto_open = False
        self._format = None

    @classmethod
    def str_to_participants_distribution_statistics_key(cls, value: str) -> STATISTICS_KEY:
        available_values = [STATISTICS_KEY.EXPERIENCE, STATISTICS_KEY.AGE]
        for v in available_values:
            if value.lower() == v.value.lower():
                return v
        available_values_message = ', '.join(list(map(lambda v: v.value, available_values)))
        raise argparse.ArgumentTypeError(f'{value} is not a valid type_dstr value. Available values: {available_values_message}')

    @classmethod
    def str_to_chart_type(cls, value: str) -> CHART_TYPE:
        try:
            return CHART_TYPE.str_to_chart_type(value)
        except ValueError as e:
            raise argparse.ArgumentTypeError(str(e))

    @classmethod
    def str_to_extension(cls, value: str) -> EXTENSION:
        available_extensions = [EXTENSION.HTML, EXTENSION.PNG]
        available_extensions_message = ', '.join(list(map(lambda e: e.value.strip('.'), available_extensions)))
        error_message = f'{value} is not a valid extension. Available values: {available_extensions_message}'
        try:
            extension = EXTENSION(value.strip('.'))
            if extension in available_extensions:
                return extension
            raise argparse.ArgumentTypeError(error_message)
        except ValueError:
            raise argparse.ArgumentTypeError(error_message)

    def configure_args(self) -> None:
        self._parser.add_argument('path', type=str, nargs=1, help='data path')
        self._parser.add_argument('plot_type', type=PLOT_TYPE.str_to_plot_type, nargs=1, help=PLOT_TYPE.description())
        self._parser.add_argument('--type_dstr', nargs='?', const=STATISTICS_KEY.EXPERIENCE,
                                  default=STATISTICS_KEY.EXPERIENCE,
                                  type=self.str_to_participants_distribution_statistics_key,
                                  help='distribution type for the participants distribution plots')
        self._parser.add_argument('--chart_type', nargs='?', const=CHART_TYPE.BAR, default=CHART_TYPE.BAR,
                                  type=self.str_to_chart_type,
                                  help='chart type for the participants distribution plots')
        self._parser.add_argument('--to_union_rare', type=self.str_to_bool, nargs='?', const=True, default=False,
                                  help='to merge the rare values for the participants distribution plots')
        self._parser.add_argument('--format', type=self.str_to_extension, nargs='?', const=EXTENSION.HTML,
                                  default=EXTENSION.HTML,
                                  help='extension for the result plots')
        self._parser.add_argument('--auto_open', type=self.str_to_bool, nargs='?', const=True, default=False,
                                  help='to open plots automatically')
        pass

    def parse_args(self) -> None:
        args = self._parser.parse_args()
        self._path = self.handle_path(args.path[0])
        self._plot_type = args.plot_type[0]
        if self._plot_type == PLOT_TYPE.PARTICIPANTS_DISTRIBUTION:
            self._type_dstr = args.type_dstr
            self._chart_type = args.chart_type
        self._to_union_rare = args.to_union_rare
        self._format = args.format
        self._auto_open = args.auto_open

    def main(self) -> None:
        self.parse_args()
        if self._plot_type == PLOT_TYPE.PARTICIPANTS_DISTRIBUTION:
            path = os.path.join(get_profile_statistics(self._path), self._type_dstr.value + EXTENSION.PICKLE.value)
            plot_profile_statistics(path, self._type_dstr, self._chart_type, to_union_rare=self._to_union_rare,
                                    format=self._format, auto_open=self._auto_open)
        elif self._plot_type == PLOT_TYPE.TASKS_DISTRIBUTION:
            plot_tasks_statistics(self._path, format=self._format, auto_open=self._auto_open)
        elif self._plot_type == PLOT_TYPE.SPLITTING_PLOTS:
            # Todo
            pass
        else:
            raise NotImplemented


if __name__ == '__main__':
    statistics_cli = PlotsCli()
    statistics_cli.main()
