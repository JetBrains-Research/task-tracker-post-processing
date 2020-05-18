[![CircleCI](https://circleci.com/gh/JetBrains-Research/codetracker-data.svg?style=shield)](https://circleci.com/gh/JetBrains-Research/codetracker-data)

# codetracker-data

### Description

The project's goal is analyzing the students' behavior while solving diverse programming tasks and creating an 
assistant system based on previous tasks' solutions. The idea is to collapse all partial solutions of each problem 
into a single graph, a solution space, and find the proper path in this graph to suggest the next steps for successor 
students.

---

### Installation

Just clone the repository and run the following commands:

1. `pip install -r requirements.txt`
2. `pip install -r dev-requirements.txt`
3. `pip install -r test-requirements.txt`

---

### Data preprocessing

The hint generation algorithm requires data in a special format. The project contains all preprocessing data steps.

#### Requirements for the source data

1. The source data have to be in the .csv format
2. Activity tracker files have prefix **ide-events**. We use [activity tracker plugin](https://plugins.jetbrains.com/plugin/8126-activity-tracker)
3. Code tracker files can have any names. We use [code-tracker-plugin](https://github.com/elena-lyulina/codetracker) in 
the same time with the activity tracker plugin
4. Columns for the activity-tracker files you can find in the [const file](https://github.com/JetBrains-Research/codetracker-data/blob/master/src/main/util/consts.py) (the **CODE_TRACKER_COLUMN** const)
5. Columns for the code-tracker files you can find in the [const file](https://github.com/JetBrains-Research/codetracker-data/blob/master/src/main/util/consts.py) (the **ACTIVITY_TRACKER_COLUMN** const)

#### Preprocessing

The right order for data preprocessing is:
1. Union activity-tracker and code-tracker files (use **preprocess_data** method from the [preprocessing.py](https://github.com/JetBrains-Research/codetracker-data/blob/master/src/main/preprocessing/preprocessing.py))
2. Find tests results for the tasks (use **run_tests** method from the [tasks_tests_handler.py](https://github.com/JetBrains-Research/codetracker-data/blob/master/src/main/splitting/tasks_tests_handler.py))
3. Splitting data (use **split_tasks_into_separate_files** method from the [splitting.py](https://github.com/JetBrains-Research/codetracker-data/blob/master/src/main/splitting/splitting.py))
4. Removing intermediate diffs (use **remove_intermediate_diffs** method from the the [intermediate_diffs_removing.py](https://github.com/JetBrains-Research/codetracker-data/blob/master/src/main/preprocessing/intermediate_diffs_removing.py))
5. Removing inefficient statements (use **remove_inefficient_statements** method from the the [inefficient_statements_removing.py](https://github.com/JetBrains-Research/codetracker-data/blob/master/src/main/preprocessing/inefficient_statements_removing.py))
6. Adding int experience column (use **add_int_experience** method from the the [int_experience_adding.py](https://github.com/JetBrains-Research/codetracker-data/blob/master/src/main/preprocessing/int_experience_adding.py))

**Note:** you can use the actions independently, but before running **N** step you have to have data after all actions for steps **[0; N - 1]** 

#### Available languages

- [x] Java
- [x] Python
- [x] Kotlin
- [x] C++

---

### Hint generation

The steps for the hint generation:
1. Construct the **Solution graph** (use **construct_solution_graph** method from the the [solution_space_handler.py](https://github.com/JetBrains-Research/codetracker-data/blob/master/src/main/solution_space/solution_space_handler.py))
2. You can serialize/deserialize a graph if you want. Use the [SolutionSpaceSerializer](https://github.com/JetBrains-Research/codetracker-data/blob/master/src/main/solution_space/solution_space_serializer.py) class
3. Get a hint by using the path finder algorithm



**Note**: you can use the [Path Finder Test System](https://github.com/JetBrains-Research/codetracker-data/blob/master/src/main/solution_space/path_finder_test_system.py) for testing all current version the path finder algorithm.
You have to create an instance of **TestSystem** for it with necessary ages, experiences and sources.


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

You can use the [SolutionSpaceVisualizer](https://github.com/JetBrains-Research/codetracker-data/blob/master/src/main/solution_space/solution_space_visualizer.py) class for graph visualization
The graph visualization process uses [Graphviz](https://www.graphviz.org/) library and additionally stores trees after 
anonymization and canonicalization process for each vertex.


#### Nodes number statistics

You can visualize nodes number in trees statistics (for each vertex and in general). You should use 
**plot_node_numbers_statistics** and **plot_node_numbers_freq_for_each_vertex** from [solution_graph_statistics_plots.py](https://github.com/JetBrains-Research/codetracker-data/blob/master/src/main/plots/solution_graph_statistics_plots.py)


---

### Run tests

We use [`pytest`](https://docs.pytest.org/en/latest/contents.html) library for tests.

__Note__: If you have `ModuleNotFoundError` while you try to run tests, please call `pip install -e .`
 before using the test system.
 
 __Note__: We use different compiles for checking tasks. You can find all of them in the [Dockerfile](https://github.com/JetBrains-Research/codetracker-data/blob/master/Dockerfile). But also we use [kotlin compiler](https://kotlinlang.org/docs/tutorials/command-line.html) for checking kotlin tasks, you need install it too if you have kotlin files

Use `python setup.py test` from the root directory to run __ALL__ tests. 
If you want to run a part of tests, please use `param --test_level`.

You can use different test levels for `param --test_level`:

Param | Description 
--- | --- 
__all__ | all tests from all modules (it is the default value)
__canon__ | tests from the canonicalization module
__solution_space__ | tests from the solution space module 
__plots__ | tests from the plots module 
__preprocess__ | tests from the preprocessing module 
__splitting__ | tests from the splitting module 
__util__ | tests from the util module 
