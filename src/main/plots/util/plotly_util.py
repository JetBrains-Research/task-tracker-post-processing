# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

import plotly
import logging

from src.main.util import consts
import plotly.graph_objects as go
from src.main.plots.util import consts as plot_consts
from src.main.util.file_util import change_extension_to
from src.main.plots.util.plots_common import create_directory_for_plots


log = logging.getLogger(consts.LOGGER_NAME)


def save_plot(fig: go.Figure, path: str, plot_type: plot_consts.PLOT_TYPE, plot_name: str = 'result_plot',
              format: consts.EXTENSION = consts.EXTENSION.HTML, auto_open: bool = False):
    file_name = create_directory_for_plots(path, plot_type, change_extension_to(plot_name, format))
    plotly.offline.plot(fig, filename=file_name, auto_open=auto_open)
