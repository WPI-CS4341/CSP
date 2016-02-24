"""
Written by Harry Liu (yliu17) and Tyler Nickerson (tjnickerson)
"""
import sys
import os.path
import pprint
from classes.bag import Bag
from classes.item import Item
from classes.constraint import Constraint
from classes.csp import CSP
from classes.solver import Solver


def main():
    # Read command line arguments
    args = sys.argv[1:]
    # More than 1 argument supplied
    if len(args) > 1:
        # Get data inputfilename
        inputfilename = args[0]
        # Bags
        bags = {}
        # Items
        items = {}
        # Section tracker
        current_section = 0
        # Read each line and add to the examples and output lists
        if os.path.isfile(inputfilename):
            with open(inputfilename, "r") as infile:
                for line in infile:
                    # If the line is a comment, increment the section counter
                    if line[:5].strip() == "#####":
                        current_section += 1
                    else:
                        # Split the line and remove all tabs, newlines, etc.
                        s = [x.strip() for x in line.split(" ")]

                        if current_section == 1:  # Items
                            name = s[0]
                            weight = s[1]
                            items[name] = Item(name, weight)
                        elif current_section == 2:  # Bags
                            name = s[0]
                            capacity = s[1]
                            bags[name] = Bag(name, capacity)
                        elif current_section == 3:  # Fitting limits
                            lower_bound = s[0]
                            upper_bound = s[1]
                            for b in bags:
                                constraint = Constraint(
                                    Constraint.BAG_FIT_LIMIT, bags=[bags[b]],
                                    min_items=lower_bound, max_items=upper_bound)
                                bags[b].constraints.append(constraint)
                        elif current_section == 4:  # Unary inclusive
                            name = s[0]
                            require_bags = [bags[k] for k in s[1:]]
                            constraint = Constraint(Constraint.UNARY_CONSTRAINT_IN_BAGS, items=[
                                items[name]], bags=require_bags)
                            items[name].constraints.append(constraint)
                        elif current_section == 5:  # Unary exclusive
                            name = s[0]
                            reject_bags = [bags[k] for k in s[1:]]
                            constraint = Constraint(Constraint.UNARY_CONSTRAINT_NOT_IN_BAGS, items=[
                                items[name]], bags=reject_bags)

                            items[name].constraints.append(constraint)
                        elif current_section == 6:  # Binary equals
                            item1 = s[0]
                            item2 = s[1]
                            constraint = Constraint(Constraint.BINARY_CONSTRAINT_EQUALITY, items=[
                                items[item1], items[item2]])
                            for i in [item1, item2]:
                                items[i].constraints.append(constraint)
                        elif current_section == 7:  # Binary not equals
                            item1 = s[0]
                            item2 = s[1]
                            constraint = Constraint(Constraint.BINARY_CONSTRAINT_INEQUALITY, items=[
                                items[item1], items[item2]])
                            for i in [item1, item2]:
                                items[i].constraints.append(constraint)
                        elif current_section == 8:  # Binary inclusive
                            item1 = s[0]
                            item2 = s[1]
                            value1 = s[2]
                            value2 = s[3]
                            constraint = Constraint(Constraint.BINARY_CONSTRAINT_INCLUSIVITY, items=[
                                items[item1], items[item2]], bags=[bags[value1], bags[value2]])
                            items[item1].constraints.append(constraint)
                            items[item2].constraints.append(constraint)

            csp = CSP(items, bags)
            solver = Solver()
            solution = solver.solve(csp)

            # Output the solution
            outputfilename = args[1]
            with open(outputfilename, 'w') as infile:
                if solution is not None:
                    keys = list(solution.keys())
                    keys.sort()
                    for bag in keys:
                        total_weight = sum(items[x].weight for x in solution[bag])
                        infile.write(bag + " " + " ".join(solution[bag]) + "\n")
                        infile.write ("number of items: " + str(len(solution[bag])) + "\n")
                        infile.write ("total weight " + str(total_weight) + "/" + str(bags[bag].capacity) + "\n")
                        infile.write ("wasted capacity: " + str(bags[bag].capacity - total_weight) + "\n")
                else:
                    infile.write ("No solution!\n")
        else:
            # Throw error when cannot open file
            print("Input file does not exist.")
    else:
        # Show usage when not providing enough argument
        print("Usage: python main.py <inputfilename> <outputfilename")


if __name__ == "__main__":
    main()
