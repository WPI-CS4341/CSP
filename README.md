# CSPs in Python
The term CSP stands for [constraint satisfaction problem](https://en.wikipedia.org/wiki/Constraint_satisfaction_problem), a problem which must be solved while satisfying a number of set constraints. In this program, we used Python 2.7 to create a constraint net that can sort items into bags. Each item has a weight, and each bag as weight and item capacity. It is the job of the constraint net to figure out how to best sort these items given a set of constraints. For more information on these constraints and how they are represented in the example files, [see here](https://sites.google.com/site/cs4341aiatwpi/projects/project-4--csp).

## Running
It is extremely simple to run the CSP solver. Just `cd` into the source directory and run:

`python main.py <filename>`

where `<filename>` is the filename of the input file. 26 test input files and their expected outputs can be found in the `test` directory.

## Under the Hood
### Search
For maximum efficiency, this program uses [backtracking search](https://en.wikipedia.org/wiki/Backtracking), partnered with [forward search](https://en.wikipedia.org/wiki/Look-ahead_(backtracking)) to reach a desired solution. This approach was chosen due to its speed, it allows for the pruning of unnecessary search nodes, minimizing the total number of possibilities that need to be explored and maximizing the speed in which a solution is found.

### Heuristics
In terms of [search heuristics](https://www.cs.unc.edu/~lazebnik/fall10/lec08_csp2.pdf), this program the minimum-remaining-values heuristic to select the next unassigned variable (item), then tries different values (bags) as sorted by the least-constraining-value heuristic.

#### MRV
The minimum-remaining-values (MRV) heuristic chooses the next variable to seek assignment by examining how many constraints that variable imposes on remaining variables, and choosing the one with the most constraints. If there is a tie, a degree heuristic is used to determine which variable will be chosen. The MRV implementation used in this program can be represented using the following pseudocode:

```
SELECT-UNASSIGNED-VARIABLE(assignment, csp):
    unassigned as a collection of currently unassigned variables
    min as first unassigned variable in collection

    count = COUNT-CONSTRAINTS(csp, unassigned)

    for each unassigned variable that is not min:
        var as current unassigned variable     
        r as number of remaining possible values for var
        n as the number of remaining values for min

        if r < n:
            min = var
        else if r = n:
            if count(var) > count(min):
                min = var

    return min
```

### LCV
The least-constraining-value (LCV) heuristic is used to sort the list of values during backtracking in the order of the least constraining to most constraining. This property is measured by how many values a given value "rules out" among other variables. In other words, the least constraining value would be a value that, when assigned to a variable, would give other variables the maximum number of options to choose from. This can be represented via the following pseudocode:

```
ORDER-DOMAIN-VALUES(var, csp):
    constraints as a collection of value constraints
    values as a collection of possible values to be selected

    for each val in values:
        count as a count of all possible values for var

        for each constraint on var:
            if the constraint is binary:
                neighbor = GET-NEIGHBOR(constraint, var)
                count += COUNT-VALID-VALUES(neighbor)
        constraints.add([value, count])
        var.value = NULL

    constraints = SORT-INCREASING(constraints, count)
    return INTERSECTION(constraints, values)
```

## Evaluation
To test the program, we ran the solver against 26 input files (all contained in the `test` directory). We found the program executed quickly, finding a solution in only a matter of seconds. However, while a number of the solutions matched the expected output files for their respective inputs, we also found that there were some solutions that arrived at answers different than those expected. In addition, we found that there were some problems which were calculated to have no solution, when in fact there was a solution. We imagine this may have been a result of an error in the program's consistency check when the backtracking algorithm terminates. However, due to time constraints, this issue could not fully investigated and may still lead to some percent error.

As a result, the solver succeeds in terms of speed, but may lack in terms of accuracy. The heuristics used in the program lend themselves to calculating solutions in a matter of seconds, however, the solutions delivered may not always be the most ideal solutions possible.

A comparison of the algorithms and heuristics used in this program can be found in the table below, running the program on the first five test files. The value for each problem denotes how many times a consistency check was run during the problem's evaluation.

Problem | Backtracking | BT+MRV | Forward Checking | FC+MRV
------- | ------------ | ------ | ---------------- | ------
1       | 1            | 1      | 1                | 1
2       | 2            | 2      | 2                | 2
3       | 3            | 3      | 3                | 3
4       | 12           | 7      | 12               | 7
5       | 18           | 18     | 18               | 18
