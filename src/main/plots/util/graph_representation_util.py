# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

# We want to get a graph representation in the dot format for the graphviz library
#
# A simple example is:
#
# digraph D {
#
#  node [shape=record fontname=Arial];
#
#   A [label = "Vertex A"]
#   B [label = "Vertex B"]
#   C [label = "Vertex C"]
#   D [label = "Vertex D"]
#   F [label = "Vertex F"]
#
#   A -> B, C, D
#   B -> F
#
# }
#
# For the graph:
#                 Vertex A
#           /         |         \
#       Vertex B    Vertex C   Vertex D
#           |
#       Vertex F
#
import os

from src.main.task_scoring.task_checker import check_call_safely
from src.main.util import consts
from src.main.util.file_util import create_file


def get_graph_representation(labels: str, graph_structure: str, font_name: str = 'Arial') -> str:
    return f'digraph  D {{\n\n' \
           f'node [shape=record fontname={font_name}];\n\n' \
           f'{labels}\n\n' \
           f'{graph_structure}' \
           f'\n\n}}'


def get_color_by_rate(rate: float) -> str:
    hue = str(rate * 0.33)
    return f'"{hue} 0.7 1.0"'


def create_dot_graph(output_folder: str, name_prefix: str, graph_representation: str,
                     output_format: consts.EXTENSION = consts.EXTENSION.PNG) -> str:
    file_path = os.path.join(output_folder, f'{name_prefix}{consts.EXTENSION.DOT.value}')
    # Create dot file
    create_file(graph_representation, file_path)
    dst_path = os.path.join(output_folder, f'{name_prefix}{output_format.value}')
    args = ['dot', f'-T{output_format.value[1:]}', file_path, '-o', dst_path]
    # Generate graph representation
    check_call_safely(args)
    return dst_path
