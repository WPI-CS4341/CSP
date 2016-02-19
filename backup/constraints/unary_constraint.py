class UnaryContraint(object):
    IN_BAGS = 1
    NOT_IN_BAGS = 2

    def __init__(self, bags, constraint_type):
        self.bags = []
        self.constraint_type = constraint_type

    def validate(self, item1):
        if self.constraint_type == IN_BAGS:
            return item.bag in self.bag
        else if self.constraint_type == NOT_IN_BAGS:
            return item.bag not in self.bag
        return False
