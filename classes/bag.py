class Bag(object):

    def __init__(self, name, capacity):
        # Name of bag
        self.name = name
        # Maximum weight of bag
        self.capacity = capacity
        # Items in the bag
        self.items = []
        # Constraints of bags
        self.constraints = []

    def __eq__(self, other):
        if isinstance(other, Bag):
            return self.name == other.name
        return NotImplemented

    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result
