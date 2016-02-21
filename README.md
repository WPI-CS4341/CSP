# CSPs in Python
The term CSP stands for [constraint satisfaction problem](https://en.wikipedia.org/wiki/Constraint_satisfaction_problem), a problem which must be solved while satisfying a number of set constraints. In this program, we used Python 2.7 to create a constraint net that can sort items into bags. Each item has a weight, and each bag as weight and item capacity. It is the job of the constraint net to figure out how to best sort these items given a set of constraints. For more information on these constraints and how they are represented in the example files, [see here](https://sites.google.com/site/cs4341aiatwpi/projects/project-4--csp).

## Running
It is extremely simple to run the CSP solver. Just `cd` into the source directory and run:

`python main.py <filename>`

where `<filename>` is the filename of the input file. 26 test input files and their expected outputs can be found in the `test` directory. Or, if you want to run every test at once, simply run:

`<CHANGE-ME>`

## Under the Hood
### Search
For maximum efficiency, this program uses [backtracking search](https://en.wikipedia.org/wiki/Backtracking), partnered with [forward search](https://en.wikipedia.org/wiki/State_space_planning#Forward_Search) to reach a desired solution. This approach was chosen due to its speed, it allows for the pruning of unnecessary search nodes, minimizing the total number of possibilities that need to be explored and maximizing the speed in which a solution is found.

`<INCLUDE-PSEUDOCODE>`

### Heuristics
In terms of [search heuristics](https://www.cs.unc.edu/~lazebnik/fall10/lec08_csp2.pdf), this program the minimum-remaining-values heuristic to select the next unassigned variable (item), then tries different values (bags) as sorted by the least-constraining-value heuristic.

#### MRV
The minimum-remaining-values (MRV) heuristic chooses the next variable to seek assignment by examining how many constraints that variable imposes on remaining variables, and choosing the one with the most constraints. If there is a tie, a degree heuristic is used to determine which variable will be chosen. The MRV implementation used in this program can be represented using the following pseudocode:

```
SELECT-UNASSIGNED-VARIABLE(self, assigned_items, csp):
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
