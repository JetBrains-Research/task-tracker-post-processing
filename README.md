[![JetBrains Research](https://jb.gg/badges/research.svg)](https://confluence.jetbrains.com/display/ALL/JetBrains+on+GitHub)
[![CircleCI](https://circleci.com/gh/JetBrains-Research/codetracker-data.svg?style=shield)](https://circleci.com/gh/JetBrains-Research/codetracker-data)

# Coding Assistant

### Description

The project's goal is analyzing the students' behavior while solving diverse programming tasks and creating an
assistant system based on previous solutions. The idea is to collapse all partial solutions of each problem
into a single graph, a solution space, and find the proper path in this graph to suggest the next steps for future
students.

---

### Installation

Simply clone the repository and run the following commands:

1. `pip install -r requirements.txt`
2. `pip install -r dev-requirements.txt`
3. `pip install -r test-requirements.txt`

---

### Run

Use `-h` option to get a help

**Required arguments:**
1. **path** - data path.
2. **action** - current action to run. Available values: **preprocessing**, **statistics**, **algo**.

A simple configuration: `python main.py path_to_files preprocessing`

Param | Description 
--- | --- 
__preprocessing__ | data preprocessing
__statistics__ | plot statistics
__algo__ | run the algo

**Optional arguments**:
- Data preprocessing:

__--level__ - use level param to set level for the action. Available levels:

**Note**: the the Nth level runs all the level before it

Param | Description 
--- | --- 
**-1**| use all preprocessing levels, default value
**0** |  merge activity-tracker and code-tracker files
**1** |  find tests results for the tasks
**2** |  split data
**3** |  remove intermediate diffs
**4** |  remove inefficient statements
**5** |  add int experience column


- Algo:

__--level__ - use level param to set level for the action. Available levels:

**Note**: the the Nth level runs all the level before it

Param | Description 
--- | --- 
**-1**|  run the path finder test system
**0** |  construct a solution graph
**1** |  run the main algo and get a hint, default value

Additional arguments:

Param | Description 
--- | --- 
**construct** |  to construct graph. It the argument is False, graph will be deserialized. Default value is `True`
**serialize** |  construct a solution graph. Default value is `False`
**viz**       |  run the main algo and get a hint, default value. Default value is `True`
**task**      |  run the main algo and get a hint, default value. Default value is `pies`. Available values can be found in `TASK.tasks_values()` if file [consts.py](https://github.com/JetBrains-Research/codetracker-data/blob/master/src/main/util/consts.py)

---

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

You can visualize some things

#### Participants distribution

**Note**: Run _before_ `split_tasks_into_separate_files` because it the use old files structure to count unique users.

Use **get_profile_statistics** method from [statistics_gathering.py](https://github.com/JetBrains-Research/codetracker-data/blob/master/src/main/statistics_gathering/statistics_gathering.py)
to get age and experience statistics. After that run **plot_profile_statistics** method from [profile_statistics_plots.py](https://github.com/JetBrains-Research/codetracker-data/blob/master/src/main/plots/profile_statistics_plots.py)
with the necessary column and options. Use serialized files with statistic as a parameter.

Two _columns type_ available:
1. STATISTICS_KEY.AGE
2. STATISTICS_KEY.EXPERIENCE

Two _charts type_ available:
1. PLOT_TYPE.BAR
2. PLOT_TYPE.PIE

Other options:
1. **to_union_rare** lets merge the rare values. The rare value means the freq of the value is less or equal 
than `STATISTICS_RARE_VALUE_THRESHOLD` from [consts.py](https://github.com/JetBrains-Research/codetracker-data/blob/master/src/main/plots/util/consts.py)
Default value for `STATISTICS_RARE_VALUE_THRESHOLD` is 2. Default value for **to_union_rare** is `False`.
2. **format** let us save output into a file in the different formats. The default value is `html` because the plots are 
interactive
3. **auto_open** lets open plots automatically. The default value is `False`.
4. **x_category_order** lets choose sort type for **X** axis. Available values store in `PLOTTY_CATEGORY_ORDER` from [consts.py](https://github.com/JetBrains-Research/codetracker-data/blob/master/src/main/plots/util/consts.py).
The default value is `PLOTTY_CATEGORY_ORDER.TOTAL_ASCENDING`.

#### Tasks distribution

**Note**: Run _after_ 'split_tasks_into_separate_files'

Use **plot_tasks_statistics** method from [tasks_statistics_plots.py](https://github.com/JetBrains-Research/codetracker-data/blob/master/src/main/plots/tasks_statistics_plots.py)
to plot tasks statistics.

Available options:
1. **plot_name** lets choose file name for save. Default value is _task_distribution_plot_.
2. **format** let us save output into a file in the different formats. The default value is `html` because the plots are 
interactive
3. **auto_open** lets open plots automatically. The default value is `False`.

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

### Run tests

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
