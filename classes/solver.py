from constraint import Constraint
import copy


class Solver(object):

    def __order_domain_values(self, item, csp):
        bags_constraints = []

        for bag in item.possible_bags.keys()[1:]:
            item.bag = item.possible_bags[bag]
            count = 0
            for constraint in item.constraints:
                cond = (constraint.constraint_type >=
                        Constraint.BINARY_CONSTRAINT_EQUALITY)
                if cond:
                    neighbor = constraint.get_neighbor(item)
                    num_bag_possible = self.__num_valid_bag(neighbor)
                    count += num_bag_possible
            bags_constraints.append([bag, count])
            item.bag = None

        sorted(bags_constraints, key=lambda bag: bag[1], reverse=True)
        return [item.possible_bags[bag[0]] for bag in bags_constraints]

    def __num_valid_bag(self, item):
        count = 0
        for bag in item.possible_bags:
            item.bag = item.possible_bags[bag]
            valid = 1
            for constraint in item.constraints:
                if not constraint.validate():
                    valid = 0
                    break
            count += valid

        item.bag = None
        return count

    def __select_unassigned_variable(self, assignment, csp):
        """Select unassigned variable with with fewest legal values"""

        # Initialize legal values for items
        unassigned_items = {item_name: csp.items[
            item_name] for item_name in csp.items if item_name not in assignment}

        # print unassigned_items
        # Get all unsigned
        unassigned_item_names = unassigned_items.keys()
        min_item_name = unassigned_item_names[0]

        # Get number of constraints of each unassigned item
        num_constraints = self.__get_num_constraints(csp, unassigned_items)

        # Find the item with least possible bags
        for item_name in unassigned_item_names[1:]:
            # Number possible_bags
            num_remaining_bag = len(unassigned_items[item_name].possible_bags)
            num_min_item = len(unassigned_items[min_item_name].possible_bags)

            # Select when have less possible bag
            if num_remaining_bag < num_min_item:
                min_item_name = item_name

            elif num_remaining_bag == num_min_item:
                # When have same number of possible bags
                if num_constraints[item_name] > num_constraints[min_item_name]:
                    # Select the one with maximum constraints
                    min_item_name = item_name

        return csp.items[min_item_name]

    def __get_num_constraints(self, csp, unassigned_item_names):
        """Get number of constraints a variable on others"""
        # Number of contraints
        num_constraints = {}
        # For all unsigned items
        for item_name in unassigned_item_names:
            # No contraints on other unsigned variable yet
            count = 0
            # Iterate through constraints
            for constraint in csp.items[item_name].constraints:
                # Binary constraints
                cond = (constraint.constraint_type >=
                        Constraint.BINARY_CONSTRAINT_EQUALITY)
                if cond:
                    # All items involved in constraint
                    for item in constraint.items:
                        # The other unassigned item
                        if item.name != item_name and item.name in unassigned_item_names:
                            # Increment number of constraints on other
                            # unassigned items
                            count += 1
            # Save number of constraints for this item
            num_constraints[item_name] = count
        # return dictionary
        return num_constraints

    def __inference(self, csp, item, bag, assignment):
        return self.__forward_checking(csp, item, bag, assignment)

    def __backtrack(self, assignment, csp):
        if len(assignment) == len(csp.items):
            return assignment

        item = self.__select_unassigned_variable(assignment, csp)

        assignment[item.name] = []
        for bag in self.__order_domain_values(item, csp):
            if self.__is_consistent(bag, item, assignment, csp):
                assignment[item.name].append(bag.name)
                inferences = self.__inference(csp, item, bag, assignment)

                if inferences is not None and len(inferences) > 0:
                    assignment.update(inferences)
                    result = self.__backtrack(assignment, csp)
                    if result is not None and len(result) > 0:
                        return result
                    for inference in inferences:
                        assignment.pop(inference)
                assignment[item.name].remove(bag.name)
        return None

    def __forward_checking(self, csp, item, bag, assignment):
        unassigned_items = {item_name: csp.items[
            item_name] for item_name in csp.items if item_name not in assignment}

        inferences = {}

        item.bag = bag
        for constraint in item.constraints:
            cond = (constraint.constraint_type >= Constraint.BINARY_CONSTRAINT_EQUALITY)
            if cond:
                neighbor = constraint.get_neighbor(item)
                possible_bags = self.__clean_up_neighbor(constraint, neighbor)
                if possible_bags is None:
                    return None

                inferences[neighbor.name] = possible_bags

        item.bag = None
        return inferences

    def __is_consistent(self, bag, item, assignment, csp):
        assigned_item_names = assignment.keys()
        for constraint in item.constraints:
            cond = (constraint.constraint_type >= Constraint.BINARY_CONSTRAINT_EQUALITY)
            if cond:
                neighbor = constraint.get_neighbor(item)
                if neighbor.name in assigned_item_names:
                    item.bag = bag

                    for neighbor_bag_name in assignment[neighbor.name]:
                        neighbor.bag = csp.bags[neighbor_bag_name]
                        if not constraint.validate():
                            neighbor.bag = None
                            item.bag = None
                            return False

                    neighbor.bag = None
                    item.bag = None
        return True

    def __clean_up_neighbor(self, constraint, item):
        possible_bags = item.possible_bags.copy()
        possible_bags_loop = item.possible_bags.copy()

        for bag in possible_bags_loop:
            item.bag = possible_bags[bag]
            if not constraint.validate():
                possible_bags.pop(bag)
        item.bag = None
        if len(possible_bags) == 0:
            return None
        return possible_bags.keys()

    def solve(self, csp):
        bt = self.__backtrack({}, csp)

        print bt

        result = {}
        for bag in csp.bags:
            result[bag] = []

        for item in bt:
            for bag in bt[item]:
                result[bag].append(item)

        return result
