import importlib
import os
import pkgutil

from src.main.solution_space.path_finder.path_finder import IPathFinder
from src.main.solution_space.solution_graph import SolutionGraph
from src.main.util.consts import TASK


# To make '__subclasses__()' work all subclasses need to be imported

pkg_dir = os.path.dirname(IPathFinder.__module__)
for (module_loader, name, ispkg) in pkgutil.iter_modules([pkg_dir]):
    importlib.import_module(name)

path_finders = IPathFinder.__subclasses__()


# maybe it's better to deserialize full graph?
task = TASK.PIES
graph = SolutionGraph(task)

code_fragments = []
