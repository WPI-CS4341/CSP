class CSP(object):
    def __init__(self, items, bags):
        self.bags = bags
        self.items = items
        
        for item_name in self.items:
            self.items[item_name].possible_bags = self.bags.copy()
