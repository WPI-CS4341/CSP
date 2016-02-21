class Item(object):

    def __init__(self, name, weight):
        # Name of the Item
        self.name = name
        # Weight of the item
        self.weight = weight
        # The bag that item is in
        self.bag = None
        # Possible bags
        self.possible_bags = []
        # Constraints of item
        self.constraints = []
