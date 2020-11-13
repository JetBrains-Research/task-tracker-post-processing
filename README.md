[![JetBrains Research](https://jb.gg/badges/research.svg)](https://confluence.jetbrains.com/display/ALL/JetBrains+on+GitHub)
[![CircleCI](https://circleci.com/gh/JetBrains-Research/codetracker-data.svg?style=shield)](https://circleci.com/gh/JetBrains-Research/codetracker-data)


# Table of Contents

- [Coding Assistant](#coding-assistant)
  - [Short description](#short-description)
  - [Detail description](#detail-description)
    - [Data preprocessing](#data-preprocessing)
    - [Hint generation](#hint-generation)
    - [Visualization](#visualization)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Data preprocessing module](#data-preprocessing-module)
    - [Plots module](#plots-module) 
    - [Hint generation module](#hint-generation-module) 
    - [Path finder test system module](#path-finder-test-system-module)   
  - [Tests running](#tests-running)        


# Coding Assistant

## Short description

The project's goal is analyzing the students' behavior while solving diverse programming tasks and creating an
assistant system based on previous solutions. The idea is to collapse all partial solutions of each problem
into a single graph, a solution space, and find the proper path in this graph to suggest the next steps for future
students.

---

## Detail description

### Data preprocessing

The hint generation algorithm requires data to have a special format. The repository contains all the necessary 
preprocessing data steps.

#### Requirements for the source data

1. The source data has to be in the .csv format.
2. _Activity-tracker files_ have a prefix **ide-events**. We use [activity-tracker plugin](https://plugins.jetbrains.com/plugin/8126-activity-tracker).
3. _Codetracker files_ can have any names. We use [codetracker-plugin](https://github.com/elena-lyulina/codetracker) at 
the same time with the activity tracker plugin.
4. Columns for the _activity-tracker files_ can be found in the [const file](src/main/util/consts.py) (the **CODE_TRACKER_COLUMN** const).
5. Columns for the _codetracker files_ can be found in the [const file](src/main/util/consts.py) (the **ACTIVITY_TRACKER_COLUMN** const).

#### Preprocessing

The correct order for data preprocessing is:
1. Do primary data preprocessing (use **preprocess_data** function from [preprocessing.py](src/main/preprocessing/preprocessing.py)).
2. Merge _codetracker files_ and _activity-tracker_ files (use **merge_ct_with_ati** function from [preprocessing.py](src/main/preprocessing/merging_ct_with_ati.py)).
3. Find tests results for the tasks (use **run_tests** function from [tasks_tests_handler.py](src/main/task_scoring/tasks_tests_handler.py)).
4. Reorganize files structure (use **reorganize_files_structure** function from [task_scoring.py](src/main/task_scoring/task_scoring.py)).
5. [Optional] Remove intermediate diffs (use **remove_intermediate_diffs** function from [intermediate_diffs_removing.py](src/main/preprocessing/intermediate_diffs_removing.py)).
6. [Optional, only for Python language] Remove inefficient statements (use **remove_inefficient_statements** function from [inefficient_statements_removing.py](src/main/preprocessing/inefficient_statements_removing.py)).
7. [Optional] Add _int experience_ column (use **add_int_experience** function from [int_experience_adding.py](src/main/preprocessing/int_experience_adding.py)).

**Note:** you can use the actions independently, the data for the Nth step must have passed all the steps before it.

#### Available languages

- [x] C++
- [x] Java
- [x] Kotlin
- [x] Python

---

### Hint generation

The steps for the hint generation:
1. Construct or deserialize a **Solution graph** (use **construct_solution_graph** function from [solution_space_handler.py](src/main/solution_space/solution_space_handler.py) or **deserialize** function from [solution_space_serializer.py](https://github.com/JetBrains-Research/codetracker-data/blob/master/src/main/solution_space/solution_space_serializer.py)).
2. Serialize the graph if you want. Use the [SolutionSpaceSerializer](src/main/solution_space/solution_space_serializer.py) class.
3. Generate a hint by using the path finder algorithm.



**Note**: you can use the [Path Finder Test System](src/main/solution_space/path_finder_test_system.py) 
for testing all current version of the path finder algorithm.
You have to create an instance of **TestSystem** for it with necessary ages, experiences, and sources.


#### Available languages

- [x] Python

---

### Visualization

You can visualize different parts of the pipeline.

#### Participants distribution

**Note**: Run _before_ 'reorganize_files_structure' because the old files structure is used to count unique users.

Use **get_profile_statistics** function from [statistics_gathering.py](src/main/statistics_gathering/statistics_gathering.py)
to get the age and experience statistics. After that, run **plot_profile_statistics** function from [profile_statistics_plots.py](src/main/plots/profile_statistics_plots.py)
with the necessary column and options. Use serialized files with statistic as a parameter.

Two column types are available:
1. STATISTICS_KEY.AGE
2. STATISTICS_KEY.EXPERIENCE

Two chart types are available:
1. CHART_TYPE.BAR
2. CHART_TYPE.PIE

Other options:
1. **to_union_rare** use to merge the rare values. The rare value means the frequency of the value is less than or equal to `STATISTICS_RARE_VALUE_THRESHOLD` from [consts.py](https://github.com/JetBrains-Research/codetracker-data/blob/master/src/main/plots/util/consts.py).
Default value for `STATISTICS_RARE_VALUE_THRESHOLD` is 2.
2. **format** use to save the output into a file in different formats. The default value is `html` because the plots are
interactive.
3. **auto_open** use to open plots automatically.
4. **x_category_order** use to choose the sort order for **X** axis. Available values are stored in `PLOTTY_CATEGORY_ORDER` from [consts.py](https://github.com/JetBrains-Research/codetracker-data/blob/master/src/main/plots/util/consts.py).
The default value is `PLOTTY_CATEGORY_ORDER.TOTAL_ASCENDING`.

#### Tasks distribution

**Note**: Run _after_ 'reorganize_files_structure'.

Use **plot_tasks_statistics** function from [tasks_statistics_plots.py](src/main/plots/tasks_statistics_plots.py)
to plot tasks statistics.

Available options:
1. **plot_name** use to choose the filename. The default value is _task_distribution_plot_.
2. **format** use to save the output into different formats. The default value is `html` because the plots are
interactive.
3. **auto_open** use to open plots automatically. 

#### Activity tracker plots

Use **create_ati_data_plot** function from [ati_data_plots](src/main/plots/ati_data_plots.py) to plot length of the current fragment together with the actions performed in IDE.



#### Scoring solutions plots

**Note**: Run _after_ 'run_tests'.

Use **plot_scoring_solutions** function from [scoring_solutions_plots.py](src/main/plots/scoring_solutions_plots.py)
to plot scoring solutions.

#### Graph visualization

You can use the [SolutionSpaceVisualizer](src/main/solution_space/solution_space_visualizer.py) 
class for graph visualization.
The graph visualization process uses [Graphviz](https://www.graphviz.org/) library and additionally stores trees after 
anonymization and canonicalization process for each vertex.


#### The number of nodes statistics

You can visualize the number of nodes in trees statistics (for each vertex and in general). You should use 
**plot_node_numbers_statistics** and **plot_node_numbers_freq_for_each_vertex** 
from [solution_graph_statistics_plots.py](src/main/plots/solution_graph_statistics_plots.py).


---

## Installation

Simply clone the repository and run the following commands:

1. `pip install -r requirements.txt`
2. `pip install -r dev-requirements.txt`
3. `pip install -r test-requirements.txt`

---

## Usage

Run the necessary file for available modules:

File| Module | Description
--- | --- | --- 
[preprocessing.py](src/main/cli/preprocessing.py) | [Data preprocessing module](#data-preprocessing-module) | Includes all steps from the [Data preprocessing](#data-preprocessing) section
[plots.py](src/main/cli/plots.py) | [Plots module](#plots-module) | Includes _Participants distribution_, _Tasks distribution_, _Activity tracker plots_, and _Scoring solutions plots_ from the [Visualization](#visualization) section
[algo.py](src/main/cli/algo.py) | [Hint generation module](#hint-generation-module) | Includes all steps from the [Hint generation](#hint-generation) section
[path_finder_test_system.py](src/main/cli/path_finder_test_system.py) | [Path finder test system module](#path-finder-test-system-module) | Run the path finder test system

A simple configuration: `python <file> <args>`

Use `-h` option to show help for each module.

### Data preprocessing module

See description: [usage](#usage)

File for running: [preprocessing.py](src/main/cli/preprocessing.py)

**Required arguments:**
1. **path** — the path to data.

**Optional arguments**:

__--level__ — use to set the level for the preprocessing. Available levels:

Value | Description
--- | ---
**0** |  primary data processing 
**1** |  merge _codetracker files_ and _activity-tracker files_
**2** |  find tests results for the tasks
**3** |  reorganize files structure 
**4** |  remove intermediate diffs
**5** |  [only for Python language] remove inefficient statements
**6** |  add _int experience_ column, default value

**Note**: the Nth level runs all the levels before it. The default value is 3.

### Plots module

See description: [usage](#usage)

File for running: [plots.py](src/main/cli/plots.py)

**Required arguments:**
1. **path** — the path to data.
2. **plot_type** — the type of plot. Available values:

Value | Description
--- | ---
**participants_distr** |  use to visualize [Participants distribution](#participants-distribution)
**tasks_distr**        |  use to visualize [Tasks distribution](#tasks-distribution)
**ati**                |  use to visualize [Activity tracker plots](#activity-tracker-plots)
**scoring**            |  use to visualize [Scoring solutions plots](#scoring-solutions-plots)

**Optional arguments**:

Parameter | Description
--- | ---
**&#8209;&#8209;type_distr**   |  distribution type. Only for **plot_type**: `participants_distr`. Available values are `programExperience` and `age`. The default value is `programExperience`.
**&#8209;&#8209;chart_type**  |  chart type. Only for **plot_type**: `participants_distr`. Available values are `bar` and `pie`. The default value is `bar`.
**&#8209;&#8209;to_union_rare**| use to merge the rare values. Only for **plot_type**: `participants_distr`.
**&#8209;&#8209;format**      |  use to save the output into a file in different formats. For all plots except **plot_type**: `ati` Available values are `html` and `png`. The default value is `html`. 
**&#8209;&#8209;auto_open**   |  use to open plots automatically.


### Hint generation module

See description: [usage](#usage)

File for running: [algo.py](src/main/cli/algo.py)

**Required arguments:**
1. **path** — the path of the folder with files to construct the solution graph or path of the serialized solution graph

**Optional arguments**:

__--level__ use to set the level for running the algorithm. Available levels:

Value | Description
--- | ---
**0** |  construct or deserialize a solution graph
**1** |  run the main algorithm and get a hint, default value

**Note**: the Nth level runs all the levels before it. The default value is the max level value.

Parameter | Description
--- | ---
**&#8209;&#8209;construct**   |  use to construct the solution graph using data from the given path. The default value is `True`
**&#8209;&#8209;deserialize** |  use to deserialize the solution graph that's stored in the path. The default value is `False`
**&#8209;&#8209;serialize**   |  use to serialize the solution graph, that was gotten after constructing/deserialization. The default value is `False`.
**&#8209;&#8209;viz**         |  use to visualize the solution graph. The default value is `True`.
**&#8209;&#8209;nod_num_stat**|  use to visualize the number of nodes in trees statistics (for each vertex and in general). The default value is `False`
**&#8209;&#8209;task**        |  the task for the main algorithm. The default value is `pies`. Available values can be found in `TASK.tasks_values()` if file [consts.py](https://github.com/JetBrains-Research/codetracker-data/blob/master/src/main/util/consts.py).

**Note**: you should use only one param from the set {**--construct**, **--deserialize**} in the same time

### Path finder test system module

See description: [usage](#usage)

File for running: [path_finder_test_system.py](src/main/cli/path_finder_test_system.py)

**Required arguments:**
1. **path** — the path of the folder with files to construct the solution graph or path of the serialized solution graph

**Optional arguments**:

Parameter | Description
--- | ---
**&#8209;&#8209;construct**   |  use to construct the solution graph using data from the given path. The default value is `True`
**&#8209;&#8209;deserialize** |  use to deserialize the solution graph that's stored in the path. The default value is `False`
**&#8209;&#8209;serialize**   |  use to serialize the solution graph, that was gotten after constructing/deserialization. The default value is `False`.
**&#8209;&#8209;viz**         |  use to visualize the solution graph. The default value is `True`
**&#8209;&#8209;nod_num_stat**|  use to visualize the number of nodes in trees statistics (for each vertex and in general). The default value is `False`
**&#8209;&#8209;task**        |  the task for the main algorithm. The default value is `pies`. Available values can be found in `TASK.tasks_values()` if file [consts.py](https://github.com/JetBrains-Research/codetracker-data/blob/master/src/main/util/consts.py).

**Note**: you should use only one param from the set {**--construct**, **--deserialize**} in the same time

---

## Tests running

We use [`pytest`](https://docs.pytest.org/en/latest/contents.html) library for tests.

__Note__: If you have `ModuleNotFoundError` while you try to run tests, please call `pip install -e .`
 before using the test system.
 
 __Note__: We use different compilers for checking tasks. You can find all of them in the [Dockerfile](Dockerfile). 
 But we also use [kotlin compiler](https://kotlinlang.org/docs/tutorials/command-line.html) for checking kotlin tasks, 
 you need to install it too if you have kotlin files.

Use `python setup.py test` from the root directory to run __ALL__ tests. 
If you want to only run some tests, please use `param --test_level`.

You can use different test levels for param `--test_level`:

Param | Description 
--- | --- 
__all__ | all tests from all modules (the default value)
__canon__ | tests from the canonicalization module
__solution_space__ | tests from the solution space module 
__plots__ | tests from the plots module 
__preprocess__ | tests from the preprocessing module 
__test_scoring__ | tests from the test scoring module 
__util__ | tests from the util module 
