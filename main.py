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
    if len(args) > 0:
        # Get data filename
        filename = args[0]
        # Bags
        bags = {}
        # Items
        items = {}
        # Section tracker
        current_section = 0
        # Read each line and add to the examples and output lists
        if os.path.isfile(filename):
            with open(filename, "r") as infile:
                for line in infile:
                    # Remove new line character and carriage return
                    line = line[:-1]
                    # If the line is a comment, increment the section counter
                    if line[:5].strip() == "#####":
                        current_section += 1
                    else:
                        s = line.split(" ")
                        if current_section == 1:  # Items
                            name = s[0]
                            weight = s[1]
                            items[name] = Item(weight)
                        elif current_section == 2:  # Bags
                            name = s[0]
                            capacity = s[1]
                            bags[name] = Bag(capacity)
                        elif current_section == 3:  # Fitting limits
                            lower_bound = s[0]
                            upper_bound = s[1]
                            constraint = Constraint(
                                Constraint.BAG_FIT_LIMIT, min_items=lower_bound, max_items=upper_bound)
                            for b in bags:
                                bags[b]["lower_bound"] = lower_bound
                                bags[b]["upper_bound"] = upper_bound
                        elif current_section == 4:  # Unary inclusive
                            name = s[0]
                            require_bags = s[1:]
                            constraint = Constraint(Constraint.UNARY_CONSTRAINT_IN_BAGS, items=[
                                                    items[name]], bags=require_bags)
                            items[name].constraints.append(constraint)
                        elif current_section == 5:  # Unary exclusive
                            name = s[0]
                            reject_bags = s[1:]
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
                            constraint = Constraint(BINARY_CONSTRAINT_INCLUSIVITY, items=[
                                                    items[item1], items[item2]], bags=[bags[value1], bags[value2]])
                            items[item1].constraints.append(constraint)
                            items[item2].constraints.append(constraint)
                pp = pprint.PrettyPrinter(indent=4)
                pp.pprint(items)
                pp.pprint(bags)

        else:
            # Throw error when cannot open file
            print("Input file does not exist.")
    else:
        # Show usage when not providing enough argument
        print("Usage: python main.py <filename>")

if __name__ == "__main__":
    main()
