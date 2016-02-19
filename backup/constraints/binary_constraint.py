class BinaryContraint(object):
    def __init__(self, bag1, bag2):
        self.bag1 = bag1
        self.bag2 = bag2

    def validate(self, item1, item2):
        if item1.bag == self.bag1:
            return item2.bag == self.bag2
        else if item1.bag == self.bag2:
            return item2.bag == self.bag1

        return True
