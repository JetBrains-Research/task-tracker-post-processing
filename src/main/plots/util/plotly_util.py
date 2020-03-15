# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import plotly
import logging

from src.main.util import consts
from src.main.plots.util import consts as plot_consts
from src.main.util.file_util import change_extension_to
from src.main.plots.util.plots_common import create_directory_for_plots


log = logging.getLogger(consts.LOGGER_NAME)


def save_plot(fig, path: str, plot_type: plot_consts.PLOT_TYPES, plot_name='result_plot',
              format=consts.EXTENSION.HTML.value, auto_open=False):
    file_name = create_directory_for_plots(path, plot_type, change_extension_to(plot_name, format))
    plotly.offline.plot(fig, filename=file_name, auto_open=auto_open)