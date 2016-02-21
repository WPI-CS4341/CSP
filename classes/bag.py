class Bag(object):

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

    def has_capcity(self, item):
        weight = reduce(self.__weight, self.items, 0)
        if item.weight + weight <= self.capacity:
            return True
        return False

    def __eq__(self, other):
        if isinstance(other, Bag):
            return self.name == other.name
        return NotImplemented

    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result
