class CSP(object):

    UNARY_CONSTRAINTS = 1
    BINARY_CONSTRAINTS = 2
    NUMBER_CONSTRAINTS = 3

    def __init__(self):
        self.items = []
        self.bags = []
        self.contraints = [2]

    def get_constraints(self, item1, item2):
        if item2 is None:
            constraints[] =
