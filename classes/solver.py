from .constraint import Constraint
import copy


class Solver(object):
    def __order_domain_values(self, item, csp, possible_bags):
        """least constraining value (MRV) heuristic"""
        # Number of constraints
        bags_constraints = []
        # Dictionary of possible bags
        item_possible_bags = possible_bags[item.name]

        # Generate list of number of constraints for each bag
        for bag in item_possible_bags:
            # Count number of neighbor's inconsistent values
            count = 0
            for constraint in item.constraints:
                # When have neighbor
                cond = (constraint.constraint_type >=
                        Constraint.BINARY_CONSTRAINT_EQUALITY)
                if cond:
                    # Get neighbor from constraint
                    neighbor = constraint.get_neighbor(item)

                    # Try put item in bag
                    item.bag = item_possible_bags[bag]
                    item_possible_bags[bag].items.append(item)

                    # Get number of inconsistent bags for current neighbor
                    num_bag_invalid = self.__num_invalid_bag(neighbor, possible_bags[neighbor.name])

                    # Restore contaminated bag
                    item_possible_bags[bag].items.remove(item)
                    item.bag = None

                    # Add neighbor's inconsistent bags
                    count += num_bag_invalid

            # Keep bag and it's number of corresponding ruled
            # out neighbor bags in list
            bags_constraints.append([csp.bags[bag], count])

        # Sort candidate bag that rules out the fewest choices
        # for the neighboring variables in the constraint graph
        sorted(bags_constraints, key=lambda bag: bag[1])

        # Preserve only values in value-count pairs
        bags = [bag[0] for bag in bags_constraints]

        # return sorted values
        return bags

    def __select_unassigned_variable(self, assignment, csp, possible_bags):
        """Select unassigned variable with with fewest legal values"""

        # Initialize legal values for items
        unassigned_items = {item_name: csp.items[
            item_name] for item_name in csp.items if item_name not in assignment}

        # Get all unsigned
        unassigned_item_names = list(unassigned_items.keys())
        min_item_name = unassigned_item_names[0]

        # Get number of constraints of each unassigned item
        num_constraints = self.__get_num_constraints(csp, unassigned_items)

        # Find the item with least possible bags
        for item_name in unassigned_item_names[1:]:
            # Number possible_bags
            num_remaining_bag = len(possible_bags[item_name])
            num_min_item = len(possible_bags[min_item_name])

            # Select when have less possible bag
            if num_remaining_bag < num_min_item:
                min_item_name = item_name

            elif num_remaining_bag == num_min_item:
                # When have same number of possible bags
                if num_constraints[item_name] >= num_constraints[min_item_name]:
                    # Select the one with maximum constraints
                    min_item_name = item_name

        # print min_item_name
        return csp.items[min_item_name]

    def __num_invalid_bag(self, item, possible_bags):
        """Get number of ruled out values"""
        # Counter
        count = 0

        # Loop through all possible values
        for bag in possible_bags:
            # Add item into bag
            item.bag = possible_bags[bag]
            possible_bags[bag].items.append(item)

            # Validate value
            for constraint in item.constraints:
                if not constraint.validate():
                    # Invalid value
                    count += 1
                    break

            # Clean up bag
            possible_bags[bag].items.remove(item)
            item.bag = None

        # return count
        return count

    def __get_num_constraints(self, csp, unassigned_item_names):
        """Get number of constraints a variable on others"""
        # Number of constraints
        num_constraints = {}
        # For all unsigned items
        for item_name in unassigned_item_names:
            # No constraints on other unsigned variable yet
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

    def __inference(self, csp, item, bag, assignment, possible_bags):
        """Make inference on neighbor"""
        # Perform forward checking on neighbors
        return self.__forward_checking(csp, item, bag, assignment, possible_bags)

    def __is_complete(self, assignment, csp):
        # Assignment complete when is true
        return len(assignment) == len(csp.items)

    def __all_bags_limit_full_test(self, csp):
        """Check whether is bag is 90% full and it's lower limit"""
        for bag in csp.bags:
            cond1 = not csp.bags[bag].is_ninety_percent_full()
            cond2 = not csp.bags[bag].fit_lower_limit()
            if cond1 or cond2:
                # Invalid assignment
                return False
        # Good assignment
        return True

    def backtrack(self, assignment, csp, possible_bags):
        # Stop when assignment completed
        if self.__is_complete(assignment, csp):
            if self.__all_bags_limit_full_test(csp):
                # Valid assignment
                return assignment
            else:
                # Fail
                return None

        # Make a copy of possible bags, preventing change that for caller
        new_possible_bags = possible_bags.copy()
        # Select an unassigned item based on minimum remaining value heuristic
        item = self.__select_unassigned_variable(assignment, csp, new_possible_bags)
        # Order possible bags based on least constraint value heuristic
        for bag in self.__order_domain_values(item, csp, new_possible_bags):
            # Check whether the value is consistent with its constraints
            if self.__is_consistent(bag, item, assignment, csp):
                # Initialize assignment dictionary
                if item.name not in assignment:
                    assignment[item.name] = []

                # Assign item with bag
                assignment[item.name].append(bag.name)
                bag.items.append(item)
                # Propagate checking through arcs, rule out inconsistent neighbor values
                inferences = self.__inference(csp, item, bag, assignment, new_possible_bags)
                if inferences is not None:
                    # Successfully made inference
                    # Try to Assignment next unassigned variable
                    result = self.backtrack(assignment, csp, new_possible_bags)
                    if result is not None:
                        # Assignment succeed
                        bag.items.remove(item)
                        # print result
                        return result

                    # Assignment fails
                    # Restored removed neighbor candidate values
                    for inference in inferences:
                        for value in inferences[inference]:
                            new_possible_bags[inference][value] = inferences[inference][value]

                # Clean up bag
                bag.items.remove(item)
                assignment[item.name].remove(bag.name)

                # Clean up assignment when not assigned
                if len(assignment[item.name]) == 0:
                    assignment.pop(item.name)
        # Assignment fail
        return None

    def __is_consistent(self, bag, item, assignment, csp):
        """Checkout whether the value is consistent with constraints"""
        if not bag.in_capacity(item):
            return False

        assigned_item_names = assignment.keys()
        for constraint in item.constraints:
            if Constraint.UNARY_CONSTRAINT_IN_BAGS <= constraint.constraint_type <= Constraint. \
                    UNARY_CONSTRAINT_NOT_IN_BAGS:
                item.bag = bag
                bag.items.append(item)
                if not constraint.validate():
                    bag.items.remove(item)
                    item.bag = None
                    return False

                item.bag = None
                bag.items.remove(item)

            elif Constraint.BINARY_CONSTRAINT_EQUALITY <= constraint.constraint_type \
                    <= Constraint.BINARY_CONSTRAINT_INCLUSIVITY:

                neighbor = constraint.get_neighbor(item)
                if neighbor.name in assigned_item_names:
                    item.bag = bag
                    bag.items.append(item)

                    for neighbor_bag_name in assignment[neighbor.name]:
                        neighbor.bag = csp.bags[neighbor_bag_name]
                        neighbor.bag.items.append(neighbor)
                        if not constraint.validate():
                            neighbor.bag.items.remove(neighbor)
                            bag.items.remove(item)
                            neighbor.bag = None
                            item.bag = None
                            return False

                        neighbor.bag.items.remove(neighbor)
                        neighbor.bag = None
                    bag.items.remove(item)
                    item.bag = None

        return True

    def __forward_checking(self, csp, item, bag, assignment, possible_bags):
        unassigned_items = {item_name: csp.items[item_name] for item_name in csp.items if item_name not in assignment}

        inferences = {}
        for constraint in item.constraints:
            if Constraint.BINARY_CONSTRAINT_EQUALITY <= constraint.constraint_type \
                    < Constraint.BINARY_CONSTRAINT_INCLUSIVITY:
                # Get neighbor of item
                neighbor = constraint.get_neighbor(item)
                # When is unassigned neighbor
                if neighbor.name in unassigned_items:
                    # Delete bag in neighbor's domain which is inconsistent with bag of current assigned item
                    # Add item into bag
                    bag.items.append(item)
                    item.bag = bag
                    invalid_bags = self.__clean_up_neighbor(constraint, neighbor, possible_bags)
                    bag.items.remove(item)
                    item.bag = None

                    # When no possible bag
                    if invalid_bags is None:
                        return None

                    # Map invalid bags to neighbor
                    inferences[neighbor.name] = invalid_bags
        return inferences

    def __clean_up_neighbor(self, constraint, item, possible_bags):
        """Remove inconsistent bags"""
        # Keep bags invalid
        invalid_bags = {}
        loop = possible_bags[item.name].copy()

        # Loop through all possible bags
        for bag in loop:
            item.bag = possible_bags[item.name][bag]
            if not constraint.validate():
                invalid_bags[bag] = possible_bags[item.name].pop(bag)
            item.bag = None
        if len(possible_bags[item.name]) == 0:
            return None

        return invalid_bags

    def solve(self, csp):
        possible_bags = {}
        for item in csp.items:
            possible_bags[item] = csp.bags.copy()

        bt = self.backtrack({}, csp, possible_bags)

        result = {}
        for bag in csp.bags:
            result[bag] = []

        if bt:
            for item in bt:
                for bag in bt[item]:
                    result[bag].append(item)
        else:
            return None
        return result
