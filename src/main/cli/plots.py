# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import os
import sys
import logging
import argparse

from src.main.plots.ati_data_plots import create_ati_data_plot
from src.main.util.file_util import get_parent_folder

sys.path.append('.')
from src.main.util import consts
from src.main.cli.util import ICli
from src.main.util.consts import EXTENSION
from src.main.cli.configs import PLOT_TYPE, PLOTS_PARAMS
from src.main.util.strings_util import add_symbol_to_begin
from src.main.plots.util.consts import STATISTICS_KEY, CHART_TYPE
from src.main.util.log_util import configure_logger, add_console_stream
from src.main.plots.tasks_statistics_plots import plot_tasks_statistics
from src.main.plots.scoring_solutions_plots import plot_scoring_solutions
from src.main.plots.profile_statistics_plots import plot_profile_statistics
from src.main.statistics_gathering.statistics_gathering import get_profile_statistics


log = logging.getLogger(consts.LOGGER_NAME)


class PlotsCli(ICli):

    def __init__(self):
        super().__init__()
        self._path = None
        self._plot_type = None
        self._type_distr = None
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
        raise argparse.ArgumentTypeError(f'{value} is not a valid {PLOTS_PARAMS.TYPE_DISTR.value} value. '
                                         f'Available values: {available_values_message}')

    @classmethod
    def str_to_chart_type(cls, value: str) -> CHART_TYPE:
        try:
            return CHART_TYPE(value.lower())
        except ValueError:
            available_values_message = ', '.join(list(map(lambda c_t: c_t.value, CHART_TYPE)))
            raise argparse.ArgumentTypeError(f'{value} is not a chart_type value. '
                                             f'Available values: {available_values_message}')

    @classmethod
    def str_to_extension(cls, value: str) -> EXTENSION:
        available_extensions = [EXTENSION.HTML, EXTENSION.PNG]
        available_extensions_message = ', '.join(list(map(lambda e: e.value.strip('.'), available_extensions)))
        error_message = f'{value} is not a valid extension. Available values: {available_extensions_message}'
        try:
            extension = EXTENSION(add_symbol_to_begin(value.rstrip('.'), '.'))
            if extension in available_extensions:
                return extension
            raise argparse.ArgumentTypeError(error_message)
        except ValueError:
            raise argparse.ArgumentTypeError(error_message)

    def configure_args(self) -> None:
        self._parser.add_argument(PLOTS_PARAMS.PATH.value, type=str, nargs=1, help='data path')
        self._parser.add_argument(PLOTS_PARAMS.PLOT_TYPE.value, type=PLOT_TYPE.str_to_plot_type, nargs=1,
                                  help=PLOT_TYPE.description())
        self._parser.add_argument(PLOTS_PARAMS.TYPE_DISTR.value, nargs='?', const=STATISTICS_KEY.EXPERIENCE,
                                  default=STATISTICS_KEY.EXPERIENCE,
                                  type=self.str_to_participants_distribution_statistics_key,
                                  help='distribution type for the participants distribution plots')
        self._parser.add_argument(PLOTS_PARAMS.CHART_TYPE.value, nargs='?', const=CHART_TYPE.BAR,
                                  default=CHART_TYPE.BAR, type=self.str_to_chart_type,
                                  help='chart type for the participants distribution plots')
        self._parser.add_argument(PLOTS_PARAMS.TO_UNION_RARE.value, type=self.str_to_bool, nargs='?',
                                  const=True, default=False,
                                  help='to merge the rare values for the participants distribution plots')
        self._parser.add_argument(PLOTS_PARAMS.FORMAT.value, type=self.str_to_extension,
                                  nargs='?', const=EXTENSION.HTML, default=EXTENSION.HTML,
                                  help='extension for the result plots')
        self._parser.add_argument(PLOTS_PARAMS.AUTO_OPEN.value, type=self.str_to_bool, nargs='?',
                                  const=True, default=False,
                                  help='to open plots automatically')

    def parse_args(self) -> None:
        args = self._parser.parse_args()
        self._plot_type = args.plot_type[0]
        if self._plot_type == PLOT_TYPE.PARTICIPANTS_DISTRIBUTION:
            self._type_distr = args.type_distr
            self._chart_type = args.chart_type
        self._to_union_rare = args.to_union_rare
        self._format = args.format
        self._auto_open = args.auto_open
        self._path = self.handle_path(args.path[0])

    def main(self) -> None:
        self.parse_args()
        if self._plot_type == PLOT_TYPE.PARTICIPANTS_DISTRIBUTION:
            path = os.path.join(get_profile_statistics(self._path), self._type_distr.value + EXTENSION.PICKLE.value)
            plot_profile_statistics(path, self._type_distr, self._chart_type, to_union_rare=self._to_union_rare,
                                    format=self._format, auto_open=self._auto_open)
        elif self._plot_type == PLOT_TYPE.TASKS_DISTRIBUTION:
            plot_tasks_statistics(self._path, format=self._format, auto_open=self._auto_open)
        elif self._plot_type == PLOT_TYPE.ATI_PLOTS:
            create_ati_data_plot(self._path, folder_to_save=get_parent_folder(self._path), to_show=self._auto_open)
        elif self._plot_type == PLOT_TYPE.SCORING_SOLUTIONS:
            plot_scoring_solutions(self._path)
        else:
            raise NotImplemented


if __name__ == '__main__':
    configure_logger(to_delete_previous_logs=True)
    add_console_stream(log)

    statistics_cli = PlotsCli()
    statistics_cli.main()
