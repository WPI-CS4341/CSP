class Contraint(object):
    # Bag fit constraint
    BAG_FIT_LIMIT = 1

    # Unary constraints
    UNARY_CONSTRAINT_IN_BAGS = 2
    UNARY_CONSTRAINT_NOT_IN_BAGS = 3

    # Binary constraints
    BINARY_CONSTRAINT_EQUANLITY = 4
    BINARY_CONSTRAINT_INEQUANLITY = 5
    BINARY_CONSTRAINT_INCLUSIVITY = 6

    def __init__(self, x, y, items, bags, constraint_type):
        """Initalize the constraint"""
        # minimum number of items in the bag
        self.x = x
        # Maximum number of items in the bag
        self.y = y
        # Related items
        self.items = items
        # Related bags
        self.bags = bags
        # Constraint types
        self.constraint_type = constraint_type

    def validate(self):
        """Validate the contraint based on constraint type"""
        if self.constraint_type == BAG_FIT_LIMIT:
            # The number of item in bag must between x and y
            return self.x <= len(self.bags[0].items) <= self.y
        else if self.constraint_type == UNARY_CONSTRAINT_IN_BAGS:
            # The item must in the bag
            return self.items[0] in self.bags[0].items
        else if self.constraint_type == UNARY_CONSTRAINT_NOT_IN_BAGS:
            # The item must not in the bag
            return self.items[0] not in self.bags[0].items
        else if self.constraint_type == BINARY_CONSTRAINT_EQUANLITY:
            # The two items must in the same bag
            return self.items[0].bag is items[1].bag
        else if self.constraint_type == BINARY_CONSTRAINT_INEQUANLITY:
            # The two items must not in the same bag
            return items[0].bag is not items[1].bag
        else if self.constraint_type == BINARY_CONSTRAINT_INCLUSIVITY:
                # Items simultaneously in a given pair of bags
                both_in_condition = items[0].bag in bags and items[1] in bags
                # Items simultaneously not in a given pair of bags
                both_not_in_condition = items[0].bag not in bags and items[1] not in bags
                return both_in_condition or both_not_in_condition
