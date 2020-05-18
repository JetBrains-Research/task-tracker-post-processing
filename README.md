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

Todo

#### Tasks distribution

Todo

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
