import CSPComponent from csp_component
class Item(CSPComponent):
    def __init__(self, weight):
        # Weight of the item
        self.weight = weight
        # The bag that item is in
        self.bag = None
        # Constraints of item
        self.constraints = []
