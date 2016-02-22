import math

class Bag(object):
    ALMOST_FULL = 0.9

    def __init__(self, name, capacity):
        # Name of bag
        self.name = name
        # Maximum weight of bag
        self.capacity = int(capacity)
        # Items in the bag
        self.items = []
        # Constraints of bags
        self.constraints = []

    def __weight(self, weight, item):
        return item.weight + weight

    def in_capcity(self, item):
        weight = reduce(self.__weight, self.items, 0)
        if math.floor(self.capacity * Bag.ALMOST_FULL) <= weight:
            return False

        if item.weight + weight <= self.capacity:

            # The bag is not full
            return True
        return False

    def bag_fit_limit(self, item):
        for constraint in self.constraints:
            # Validate number of items in the bag
            self.items.append(item)
            if not constraint.validate():
                self.items.remove(item)
                return False
            self.items.remove(item)
        return True

    def __eq__(self, other):
        if isinstance(other, Bag):
            return self.name == other.name
        return NotImplemented

    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result
