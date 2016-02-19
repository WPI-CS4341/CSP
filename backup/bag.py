import CSPComponent from csp_component
class Bag(CSPComponent):
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []
