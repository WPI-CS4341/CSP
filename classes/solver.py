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
            vdict[current_bag.name] = violations
        items[var] = original_bag
        return sorted(vdict, key=lambda k: vdict[k])

    # Should return key name of variable
    def __select_unassigned_variable(self, csp):
        return csp.items["A"].name

    def __inference(self, csp, var, value):
        return {}

    """
    order_domain_values = LCV
    select_unassigned_variable = MRV + degree
    inference = Forward Checking
    """
    def __backtrack(self, csp):
        # if assignment is
        var = self.__select_unassigned_variable(csp)
        print self.__order_domain_values(var, csp)
        # for value in __order_domain_values(var, csp):
        #     if True:
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

    def solve(self, csp):
        bt = self.__backtrack(csp)
