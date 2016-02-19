class Solver(object):
    def __order_domain_values(self):
        return {}

    def __select_unassigned_variable(csp):
        return 0

    def __inference(csp, var, value):
        return {}

    """
    order_domain_values = LCV
    select_unassigned_variable = MRV + degree
    inference = Forward Checking
    """
    def Backtrack(assignment, csp):
        # if assignment is
        var = __select_unassigned_variable(csp)
        for value in __order_domain_values(var, assignment, csp):
            if True:
                # if value is consistent with assignment
                assignment[var] = value
                inferences = __inference(csp, var, value)
                if inferences:
                    assignment.append(inferences)  # Won't work
                    result = self.Backtrack(assignment, csp)
                    if result:
                        return result
            assignment.pop(var, None)
            assignment.pop(inferences, None)  # Won't work