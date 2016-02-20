from item import Item
from bag import Bag


class Constraint(object):
    # Bag fit constraint
    BAG_FIT_LIMIT = 1

    # Unary constraints
    UNARY_CONSTRAINT_IN_BAGS = 2
    UNARY_CONSTRAINT_NOT_IN_BAGS = 3

    # Binary constraints
    BINARY_CONSTRAINT_EQUALITY = 4
    BINARY_CONSTRAINT_INEQUALITY = 5
    BINARY_CONSTRAINT_INCLUSIVITY = 6

    def __init__(self, constraint_type, min_items=-1, max_items=-1, items={}, bags={}):
        """Initalize the constraint"""
        # minimum number of items in the bag
        self.min_items = min_items
        # Maximum number of items in the bag
        self.max_items = max_items
        # Related items
        self.items = items
        # Related bags
        self.bags = bags
        # Constraint types
        self.constraint_type = constraint_type

    def validate(self):
        """Validate the contraint based on constraint type"""
        if self.constraint_type == BAG_FIT_LIMIT:
            # Check for required variables
            if self.min_items < 0 or self.max_items < 0:
                raise ValueError("Constraint type BAG_FIT_LIMIT requires \
                    non-negative min_items and max_items values")
            # The number of item in bag must between x and y
            return self.min_items <= len(self.bags[0].items) <= self.max_items
        elif self.constraint_type == UNARY_CONSTRAINT_IN_BAGS:
            # Check for required variables
            if len(self.items) < 1 or len(self.bags) < 1:
                raise ValueError("Constraint type UNARY_CONSTRAINT_IN_BAGS \
                    requires one item and one bag")
            # The item must in the bag
            return self.items[0] in self.bags[0].items
        elif self.constraint_type == UNARY_CONSTRAINT_NOT_IN_BAGS:
            # Check for required variables
            if len(self.items) < 1 or len(self.bags) < 1:
                raise ValueError("Constraint type UNARY_CONSTRAINT_NOT_IN_BAGS \
                    requires one item and one bag")
            # The item must not in the bag
            return self.items[0] not in self.bags[0].items
        elif self.constraint_type == BINARY_CONSTRAINT_EQUALITY:
            # Check for required variables
            if len(self.items) < 2:
                raise ValueError("Constraint type BINARY_CONSTRAINT_EQUALITY \
                    requires two items")
            # The two items must in the same bag
            return self.items[0].bag is self.items[1].bag
        elif self.constraint_type == BINARY_CONSTRAINT_INEQUALITY:
            # Check for required variables
            if len(self.items) < 2:
                raise ValueError("Constraint type BINARY_CONSTRAINT_INEQUALITY \
                    requires two items")
            # The two items must not in the same bag
            return self.items[0].bag is not self.items[1].bag
        elif self.constraint_type == BINARY_CONSTRAINT_INCLUSIVITY:
                # Check for required variables
            if len(self.items) < 2 or len(self.bags) < 0:
                raise ValueError("Constraint type BINARY_CONSTRAINT_INCLUSIVITY \
                        requires two items and at least one bag")
            # Items simultaneously in a given pair of bags
            both_in_condition = items[
                0].bag in self.bags and items[1].bag in self.bags
            # Items simultaneously not in a given pair of bags
            both_not_in_condition = items[
                0].bag not in self.bags and items[1].bag not in self.bags
            return both_in_condition or both_not_in_condition
