from constraint import Constraint
import copy


class Solver(object):

    def __count_valid_domain(self, var, items, bags):
        item = var
        valid_i = 0
        for b in bags:
            bag = bags[b]
            item.putInBag(bag)
            valid_b = True
            for ic in item.constraints:
                if ic.validate() is False:
                    valid_b = False
            # for bc in bag.constraints:
            #     if bc.validate() is False:
            #         valid_b = False
            if valid_b:
                valid_i += 1
            print item.bag.name + ": " + str(valid_b)
        return valid_i

    def __order_domain_values(self, var, csp):
        bags = csp.bags
        items = csp.items
        item = var
        vdict = {}
        for b in bags:
            total = 0
            count = 0
            item.putInBag(bags[b])
            for i in csp.items:
                # print items[i].name
                # print self.__count_valid_domain(var, items, bags)
                total += self.__count_valid_domain(var, items, bags)
                count += 1
            vdict[b] = round(total / (count * 1.0))
            # print total
        return vdict

    # Should return key name of variable
    def __select_unassigned_variable(self, assigned_items, csp):
        """Select unassigned variable with with fewest legal values"""
        # Initialize legal values for items
        unassigned_items = {item_name: csp.items[
            item_name] for item_name in csp.items if item_name not in assigned_items}
        # print unassigned_items
        # Get all unsigned
        unassigned_item_names = unassigned_items.keys()
        min_item_name = unassigned_item_names[0]

        num_constrains = self.__get_num_constrains(csp, unassigned_items)

        for item_name in unassigned_item_names[1:]:
            num_remaining_bag = len(unassigned_items[item_name].possible_bags)
            num_min_item = len(unassigned_items[item_name].possible_bags)

            if num_remaining_bag < num_min_item:
                min_item_name = item_name
            else:
                if num_constrains[item_name] > num_constrains[min_item_name]:
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

        print self.__order_domain_values(var, csp)
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

    def __forward_checking(self, csp, var, value):
        return None

    def solve(self, csp):
        bt = self.__backtrack({}, csp)
