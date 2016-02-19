import CSPComponent from csp_component
class Bag(CSPComponent):
    def __init__(self, capacity):
        # Maximum weight of bag
        self.capacity = capacity
        # Items in the bag
        self.items = []
