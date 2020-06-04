[![JetBrains Research](https://jb.gg/badges/research.svg)](https://confluence.jetbrains.com/display/ALL/JetBrains+on+GitHub)
[![CircleCI](https://circleci.com/gh/JetBrains-Research/codetracker-data.svg?style=shield)](https://circleci.com/gh/JetBrains-Research/codetracker-data)

# Coding Assistant

### Description

The project's goal is analyzing the students' behavior while solving diverse programming tasks and creating an
assistant system based on previous solutions. The idea is to collapse all partial solutions of each problem
into a single graph, a solution space, and find the proper path in this graph to suggest the next steps for future
students.

---

## Modules

### Data preprocessing

The hint generation algorithm requires data to have a special format. The repository contains all the necessary 
preprocessing data steps.

#### Requirements for the source data

1. The source data has to be in the .csv format.
2. Activity tracker files have a prefix **ide-events**. We use [activity tracker plugin](https://plugins.jetbrains.com/plugin/8126-activity-tracker).
3. Code tracker files can have any names. We use [code-tracker-plugin](https://github.com/elena-lyulina/codetracker) at 
the same time with the activity tracker plugin.
4. Columns for the activity-tracker files can be found in the [const file](https://github.com/JetBrains-Research/codetracker-data/blob/master/src/main/util/consts.py) (the **CODE_TRACKER_COLUMN** const).
5. Columns for the code-tracker files can be found in the [const file](https://github.com/JetBrains-Research/codetracker-data/blob/master/src/main/util/consts.py) (the **ACTIVITY_TRACKER_COLUMN** const).

#### Preprocessing

The correct order for data preprocessing is:
1. Merge activity-tracker and code-tracker files (use **preprocess_data** method from [preprocessing.py](https://github.com/JetBrains-Research/codetracker-data/blob/master/src/main/preprocessing/preprocessing.py)).
2. Find tests results for the tasks (use **run_tests** method from [tasks_tests_handler.py](https://github.com/JetBrains-Research/codetracker-data/blob/master/src/main/splitting/tasks_tests_handler.py)).
3. Split data (use **split_tasks_into_separate_files** method from [splitting.py](https://github.com/JetBrains-Research/codetracker-data/blob/master/src/main/splitting/splitting.py)).
4. Remove intermediate diffs (use **remove_intermediate_diffs** method from [intermediate_diffs_removing.py](https://github.com/JetBrains-Research/codetracker-data/blob/master/src/main/preprocessing/intermediate_diffs_removing.py)).
5. Remove inefficient statements (use **remove_inefficient_statements** method from [inefficient_statements_removing.py](https://github.com/JetBrains-Research/codetracker-data/blob/master/src/main/preprocessing/inefficient_statements_removing.py)).
6. Add _int experience_ column (use **add_int_experience** method from [int_experience_adding.py](https://github.com/JetBrains-Research/codetracker-data/blob/master/src/main/preprocessing/int_experience_adding.py)).

**Note:** you can use the actions independently, the data for the Nth step must have passed all the steps before it.

#### Available languages

- [x] C++
- [x] Java
- [x] Kotlin
- [x] Python

---

### Hint generation

The steps for the hint generation:
1. Construct the **Solution graph** (use **construct_solution_graph** method from [solution_space_handler.py](https://github.com/JetBrains-Research/codetracker-data/blob/master/src/main/solution_space/solution_space_handler.py)).
2. Serialize/deserialize the graph if you want. Use the [SolutionSpaceSerializer](https://github.com/JetBrains-Research/codetracker-data/blob/master/src/main/solution_space/solution_space_serializer.py) class.
3. Generate a hint by using the path finder algorithm.



**Note**: you can use the [Path Finder Test System](https://github.com/JetBrains-Research/codetracker-data/blob/master/src/main/solution_space/path_finder_test_system.py) 
for testing all current version of the path finder algorithm.
You have to create an instance of **TestSystem** for it with necessary ages, experiences, and sources.


#### Available languages

- [x] Python

---

### Visualization

You can visualize different parts of the pipeline.

#### Participants distribution

**Note**: Run _before_ 'split_tasks_into_separate_files' because the old files structure is used to count unique users.

Use **get_profile_statistics** method from [statistics_gathering.py](https://github.com/JetBrains-Research/codetracker-data/blob/master/src/main/statistics_gathering/statistics_gathering.py)
to get the age and experience statistics. After that, run **plot_profile_statistics** method from [profile_statistics_plots.py](https://github.com/JetBrains-Research/codetracker-data/blob/master/src/main/plots/profile_statistics_plots.py)
with the necessary column and options. Use serialized files with statistic as a parameter.

Two column types are available:
1. STATISTICS_KEY.AGE
2. STATISTICS_KEY.EXPERIENCE

Two chart types are available:
1. PLOT_TYPE.BAR
2. PLOT_TYPE.PIE

Other options:
1. **to_union_rare** allows to merge the rare values. The rare value means the frequency of the value is less than or equal to `STATISTICS_RARE_VALUE_THRESHOLD` from [consts.py](https://github.com/JetBrains-Research/codetracker-data/blob/master/src/main/plots/util/consts.py).
Default value for `STATISTICS_RARE_VALUE_THRESHOLD` is 2. Default value for **to_union_rare** is `False`.
2. **format** allows to save the output into a file in different formats. The default value is `html` because the plots are
interactive.
3. **auto_open** allows to open plots automatically. The default value is `False`.
4. **x_category_order** allows to choose the sort order for **X** axis. Available values are stored in `PLOTTY_CATEGORY_ORDER` from [consts.py](https://github.com/JetBrains-Research/codetracker-data/blob/master/src/main/plots/util/consts.py).
The default value is `PLOTTY_CATEGORY_ORDER.TOTAL_ASCENDING`.

#### Tasks distribution

**Note**: Run _after_ 'split_tasks_into_separate_files'.

Use **plot_tasks_statistics** method from [tasks_statistics_plots.py](https://github.com/JetBrains-Research/codetracker-data/blob/master/src/main/plots/tasks_statistics_plots.py)
to plot tasks statistics.

Available options:
1. **plot_name** allows to choose the filename. The default value is _task_distribution_plot_.
2. **format** allows to save the output into different formats. The default value is `html` because the plots are
interactive.
3. **auto_open** allows to open plots automatically. The default value is `False`.

#### Splitting plots

Todo


#### Graph visualization

You can use the [SolutionSpaceVisualizer](https://github.com/JetBrains-Research/codetracker-data/blob/master/src/main/solution_space/solution_space_visualizer.py) 
class for graph visualization.
The graph visualization process uses [Graphviz](https://www.graphviz.org/) library and additionally stores trees after 
anonymization and canonicalization process for each vertex.


#### The number of nodes statistics

You can visualize the number of nodes in trees statistics (for each vertex and in general). You should use 
**plot_node_numbers_statistics** and **plot_node_numbers_freq_for_each_vertex** 
from [solution_graph_statistics_plots.py](https://github.com/JetBrains-Research/codetracker-data/blob/master/src/main/plots/solution_graph_statistics_plots.py).


---

### Installation

Simply clone the repository and run the following commands:

1. `pip install -r requirements.txt`
2. `pip install -r dev-requirements.txt`
3. `pip install -r test-requirements.txt`

---

### Running

Run the necessary file for available modules:

File| Module | Description
--- | --- | --- 
[preprocessing_main.py](https://github.com/JetBrains-Research/codetracker-data/blob/master/src/main/cli/preprocessing_main.py) | [Data preprocessing module](#data-preprocessing-module) | Includes all steps from the [Data preprocessing](#data-preprocessing) section
[statistics_main.py](https://github.com/JetBrains-Research/codetracker-data/blob/master/src/main/cli/statistics_main.py) | [Statistics module](#statistics-module) | Includes _Participants distribution_, _Tasks distribution_ and _Splitting plots_ from the [Visualization](#visualization) section
[algo_main.py](https://github.com/JetBrains-Research/codetracker-data/blob/master/src/main/cli/algo_main.py) | [Hint generation module](#hint-generation-module) | Includes all steps from the [Hint generation](#hint-generation) section
[test_system_main.py](https://github.com/JetBrains-Research/codetracker-data/blob/master/src/main/cli/test_system_main.py) | [Path finder test system module](#path-finder-test-system-module) | Run the path finder test system

A simple configuration: `python file args`

Use `-h` option to show help for each module.

#### Data preprocessing module

**Required arguments:**
1. **path** — the path to data.

**Optional arguments**:

__--level__ — allows to set the level for the preprocessing. Available levels:

Value | Description
--- | ---
**0** |  merge activity-tracker and code-tracker files
**1** |  find tests results for the tasks
**2** |  split the data
**3** |  remove intermediate diffs
**4** |  remove inefficient statements
**5** |  add _int experience_ column, default value

**Note**: the Nth level runs all the levels before it. The default value is the max level value.

#### Statistics module

_TODO_

#### Hint generation module

**Required arguments:**
1. **path** — the path of the folder with files to construct the solution graph or path of the serialized solution graph

**Optional arguments**:

__--level__ allows to set the level for running the algorithm. Available levels:

Value | Description
--- | ---
**0** |  construct a solution graph
**1** |  run the main algorithm and get a hint, default value

**Note**: the Nth level runs all the levels before it. The default value is the max level value.

Parameter | Description
--- | ---
**--construct**   |  construct the solution graph. The default value is `True`
**--deserialize** |  deserialize the solution graph. The default value is `False`
**--serialize**   |  serialize the solution graph. The default value is `False`.
**--viz**         |  visualize the solution graph. The default value is `True`
**--task**        |  the task for the main algorithm. The default value is `pies`. Available values can be found in `TASK.tasks_values()` if file [consts.py](https://github.com/JetBrains-Research/codetracker-data/blob/master/src/main/util/consts.py).

**Note**: you should use only one param from the set {**--construct**, **--deserialize**} in the same time

#### Path finder test system module

**Required arguments:**
1. **path** — the path of the folder with files to construct the solution graph or path of the serialized solution graph

**Optional arguments**:

Parameter | Description
--- | ---
**--construct**   |  construct the solution graph. The default value is `True`
**--deserialize** |  deserialize the solution graph. The default value is `False`
**--serialize**   |  serialize the solution graph. The default value is `False`.
**--viz**         |  visualize the solution graph. The default value is `True`
**--task**        |  the task for the main algorithm. The default value is `pies`. Available values can be found in `TASK.tasks_values()` if file [consts.py](https://github.com/JetBrains-Research/codetracker-data/blob/master/src/main/util/consts.py).

**Note**: you should use only one param from the set {**--construct**, **--deserialize**} in the same time

---

### Tests running

We use [`pytest`](https://docs.pytest.org/en/latest/contents.html) library for tests.

__Note__: If you have `ModuleNotFoundError` while you try to run tests, please call `pip install -e .`
 before using the test system.
 
 __Note__: We use different compilers for checking tasks. You can find all of them in the [Dockerfile](https://github.com/JetBrains-Research/codetracker-data/blob/master/Dockerfile). 
 But we also use [kotlin compiler](https://kotlinlang.org/docs/tutorials/command-line.html) for checking kotlin tasks, 
 you need to install it too if you have kotlin files.

Use `python setup.py test` from the root directory to run __ALL__ tests. 
If you want to only run some tests, please use `param --test_level`.

You can use different test levels for `param --test_level`:

Param | Description 
--- | --- 
__all__ | all tests from all modules (the default value)
__canon__ | tests from the canonicalization module
__solution_space__ | tests from the solution space module 
__plots__ | tests from the plots module 
__preprocess__ | tests from the preprocessing module 
__splitting__ | tests from the splitting module 
__util__ | tests from the util module 
