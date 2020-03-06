import logging
import plotly.graph_objects as go


from src.main.util import consts
from src.main.plots import consts as plot_consts
from src.main.plots.plotly_util import save_plot
from src.main.statistics_gathering.statistics_gathering import get_tasks_statistics
from src.main.plots.plots_common import get_readable_key


log = logging.getLogger(consts.LOGGER_NAME)


def __get_tasks_with_freq(language_dict: dict):
    tasks = []
    freq = []
    for task, cur_freq in language_dict.items():
        tasks.append(get_readable_key(task.value))
        freq.append(cur_freq)
    return tasks, freq


def __get_bars_for_plot(statistics_dict: dict):
    bars = []
    languages = statistics_dict.keys()
    for language in languages:
        tasks, freq = __get_tasks_with_freq(statistics_dict[language])
        bars.append(go.Bar(name=get_readable_key(language.value), x=tasks, y=freq))
    return bars


def __get_colors():
    colors = plot_consts.BAR_PALETTE
    # At the end of the list we have more dark colours
    colors.reverse()
    return colors


def __plot_bar_chart(bars: list, path: str, plot_name='task_plot', format=consts.EXTENSION.HTML.value,
                     auto_open=False):
    fig = go.Figure(data=bars)
    fig.update_layout(
        barmode='group',
        plot_bgcolor=plot_consts.STATISTICS_COLORS.BAR_CHART_BG.value,
        title_text='Tasks and languages distribution',
        yaxis=dict(
            title_text=plot_consts.STATISTICS_SHOWING_KEY.FREQ.value
        ),
        xaxis=dict(
            title_text='Task'
        ),
        colorway=__get_colors()
    )
    save_plot(fig, path, plot_consts.PLOT_TYPES.BAR.value, plot_name, format, auto_open)


def plot_tasks_statistics(path: str, plot_name='result_plot', format=consts.EXTENSION.HTML.value,
                          auto_open=False):
    statistics_dict = get_tasks_statistics(path)
    bars = __get_bars_for_plot(statistics_dict)
    __plot_bar_chart(bars, path, plot_name, format, auto_open)