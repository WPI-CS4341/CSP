class Item(object):

    def __init__(self, name, weight):
        # Name of the Item
        self.name = name
        # Weight of the item
        self.weight = int(weight)
        # The bag that item is in
        self.bag = None
        # Possible bags
        self.possible_bags = {}
        # Constraints of item
        self.constraints = []

    def __eq__(self, other):
        if isinstance(other, Item):
            return self.name == other.name
        return NotImplemented

    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result

    def putInBag(self, bag):
        if self.bag:
            self.bag.items = [s for s in self.bag.items if s.name is not self.name]
        bag.items.append(self)
        self.bag = bag
