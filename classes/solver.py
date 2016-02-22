from constraint import Constraint
import copy


class Solver(object):

    def __order_domain_values(self, item, csp):
        bags_constraints = []

        possible_bags = self.__possible_bags(item, csp)


        # print possible_bags
        for bag in possible_bags:
            possible_bags[bag]
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
        bags = [possible_bags[bag[0]] for bag in bags_constraints]
        # print item.name
        # print bags
        return bags

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

        # Get all unsigned
        unassigned_item_names = unassigned_items.keys()
        min_item_name = unassigned_item_names[0]

        # Get number of constraints of each unassigned item
        num_constraints = self.__get_num_constraints(csp, unassigned_items)

        # Find the item with least possible bags
        for item_name in unassigned_item_names[1:]:
            # Number possible_bags
            num_remaining_bag = len(self.__possible_bags(unassigned_items[item_name], csp))
            num_min_item = len(self.__possible_bags(unassigned_items[min_item_name], csp))

            # Select when have less possible bag
            if num_remaining_bag < num_min_item:
                min_item_name = item_name

            elif num_remaining_bag == num_min_item:
                # When have same number of possible bags
                if num_constraints[item_name] > num_constraints[min_item_name]:
                    # Select the one with maximum constraints
                    min_item_name = item_name

        # print min_item_name
        return csp.items[min_item_name]

    def __possible_bags(self, item, csp):
        bags = {}
        for bag in csp.bags:
            if csp.bags[bag].has_capcity(item):
                # print item.name + " " + bag
                bags[bag] = csp.bags[bag]

        return bags

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

    def __complete(self, assignment, csp):
        # print assignment
        return len(assignment) == len(csp.items)

    def __backtrack(self, assignment, csp):
        if self.__complete(assignment, csp):
            return assignment

        csp = copy.deepcopy(csp)
        item = self.__select_unassigned_variable(assignment, csp)

        for bag in self.__order_domain_values(item, csp):
            if self.__is_consistant(bag, item, assignment, csp):

                if item.name not in assignment:
                    assignment[item.name] = []

                assignment[item.name].append(bag.name)
                bag.items.append(item)

                inferences = self.__inference(csp, item, bag, assignment)
                if inferences is not None:
                    assignment.update(inferences)
                    # print assignment
                    result = self.__backtrack(assignment, csp)

                    # print assignment
                    # print result
                    # print ""

                    if result is not None:
                        # print result
                        return result
                    for inference in inferences:
                        assignment.pop(inference)

                bag.items.remove(item)
                assignment[item.name].remove(bag.name)
                if len(assignment[item.name]) == 0:
                    assignment.pop(item.name)
        return None

    def __forward_checking(self, csp, item, bag, assignment):
        unassigned_items = {item_name: csp.items[
            item_name] for item_name in csp.items if item_name not in assignment}

        inferences = {}
        item.bag = bag
        for constraint in item.constraints:
            cond = (constraint.constraint_type >=
                    Constraint.BINARY_CONSTRAINT_EQUALITY)
            if cond:
                neighbor = constraint.get_neighbor(item)
                possible_bags = self.__clean_up_neighbor(constraint, neighbor, csp)
                if possible_bags is None:
                    return None

                inferences[neighbor.name] = possible_bags

        item.bag = None
        return inferences

    def __is_consistant(self, bag, item, assignment, csp):
        if not bag.has_capcity(item):
            return False

        assigned_item_names = assignment.keys()
        for constraint in item.constraints:
            cond = (constraint.constraint_type >=
                    Constraint.BINARY_CONSTRAINT_EQUALITY)
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

    def __clean_up_neighbor(self, constraint, item, csp):
        print "+++++++++++++++++"
        possible_bags = item
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
