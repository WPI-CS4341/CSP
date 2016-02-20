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
