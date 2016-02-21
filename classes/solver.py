from constraint import Constraint
import copy

class Solver(object):

    def __order_domain_values(self, item, csp):
        bags_constrains = []

        for bag in item.possible_bags.keys()[1:]:
            item.bag = item.possible_bags[bag]
            count = 0
            for constraint in item.constraints:
                cond = (constraint.constraint_type >= Constraint.BINARY_CONSTRAINT_EQUALITY)
                if cond:
                    neighbor = constraint.get_neighbor(item)
                    num_bag_possible = self.__num_valid_bag(neighbor)
                    count += num_bag_possible
            bags_constrains.append([bag, count])

        return sorted(bags_constrains, key=lambda bag: bag[1], reverse=True)

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
        return count

    # Should return key name of variable
    def __select_unassigned_variable(self, assigned_items, csp):
        """Select unassigned variable with with fewest legal values"""
        # Initialize legal values for items
        unassigned_items = {item_name: csp.items[item_name] for item_name in csp.items if item_name not in assigned_items}
        # print unassigned_items
        # Get all unsigned
        unassigned_item_names = unassigned_items.keys()
        min_item_name = unassigned_item_names[0]

        # Get number of constraints of each unassigned item
        num_constrains = self.__get_num_constrains(csp, unassigned_items)

        # Find the item with least possible bags
        for item_name in unassigned_item_names[1:]:
            # Number possible_bags
            num_remaining_bag = len(unassigned_items[item_name].possible_bags)
            num_min_item = len(unassigned_items[item_name].possible_bags)

            # Select when have less possible bag
            if num_remaining_bag < num_min_item:
                min_item_name = item_name
            elif num_remaining_bag == num_min_item:
                # When have same number of possible bags
                if num_constrains[item_name] > num_constrains[min_item_name]:
                    # Select the one with maximum constraints
                    min_item_name = item_name

        return csp.items[min_item_name]

    def __get_num_constrains(self, csp, unassigned_item_names):
        """Get number of constraints a variable on others"""
        # Number of contraints
        num_constrains = {}
        # For all unsigned items
        for item_name in unassigned_item_names:
            # No contraints on other unsigned variable yet
            count = 0
            # Iterate through constraints
            for constraint in csp.items[item_name].constraints:
                # Binary constraints
                cond = (constraint.constraint_type >= Constraint.BINARY_CONSTRAINT_EQUALITY)
                if cond:
                    # All items involved in constraint
                    for item in constraint.items:
                        # The other unassigned item
                        if item.name != item_name and item.name in unassigned_item_names:
                            # Increment number of constraints on other unassigned items
                            count += 1
            # Save number of constraints for this item
            num_constrains[item_name] = count
        # return dictionary
        return num_constrains

    def __inference(self, csp, var, value):
        return __forward_checking(csp, var, value)

    """
    order_domain_values = LCV
    select_unassigned_variable = MRV + degree
    inference = Forward Checking
    """
    def __backtrack(self, assigned_items, csp):
        if len(assigned_items) == len(csp.items):
            return assigned_items

        csp = copy.deepcopy(csp)
        item = self.__select_unassigned_variable(assigned_items, csp)
        # for
        print self.__order_domain_values(item, csp)
        # for bag in __order_domain_values(var, csp):
        # if True:
        #         # if value is consistent with assignment
        #         assignment[var] = value
        #         inferences = __inference(csp, var, value)
        #         if inferences:
        #             assignment.append(inferences)  # Won't work
        #             result = self.backtrack(csp)
        #             if result:
        #                 return result
        #     assignment.pop(var, None)
        #     assignment.pop(inferences, None)  # Won't work

    def __forward_checking(self, csp, var, value):
        return None

    def solve(self, csp):
        bt = self.__backtrack({}, csp)
