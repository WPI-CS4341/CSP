class BagFitLimitContraint(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def validate(self, bag)
        return self.x <= len(bag.items) <= self.y
