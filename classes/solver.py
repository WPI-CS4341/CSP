from constraint import Constraint

class Solver(object):

    def __order_domain_values(self, var, csp):
        bags = csp.bags
        items = csp.items
        original_bag = csp.items[var].bag
        vdict = {}
        for b in bags:
            current_bag = bags[b]
            csp.items[var].bag = current_bag
            violations = 0
            for c in items[var].constraints:
                if c.validate() is False:
                    violations += 1
            vdict[current_bag] = violations
        items[var] = original_bag
        return sorted(vdict, key=lambda k: vdict[k])

    # Should return key name of variable
    def __select_unassigned_variable(self, csp):
        """Select unassigned variable with with fewest legal values"""
        # Get all unsigned
        unassigned_item_names = self.consistent_bags.keys()
        min_item_name = unassigned_item_names[0]

        num_constrains = self.__get_num_constrains(csp, unassigned_item_names)

        for item_name in unassigned_item_names[1:]:
            num_remaining_bag = len(self.consistent_bags[item_name])
            num_min_item = len(self.consistent_bags[item_name])

            if num_remaining_bag < num_min_item:
                min_item_name = item_name
            else :
                if num_constrains[item_name] > num_constrains[min_item_name]:
                    min_item_name = item_name

        self.consistent_bags.pop(min_item_name)
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
    def __backtrack(self, items,csp):
        # if assignment is
        var = self.__select_unassigned_variable(csp)
        print var.name
        # for
        # print self.__order_domain_values(var, csp)
        # for value in __order_domain_values(var, csp):
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

    # def __forward_checking(self, csp, var, value):


    def solve(self, csp):

        # Initialize legal values for items
        self.consistent_bags = {item:csp.bags.copy() for item in csp.items}

        bt = self.__backtrack([], csp)
