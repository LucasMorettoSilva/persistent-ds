from abc import ABC


class Leaf(ABC):

    def __init__(self, parent=None, value=None):
        if parent is None:
            self.parent = self
            self.depth  = 0
        else:
            self.parent = parent
            self.depth  = self.parent.depth + 1
        self.value = value
        self.jump  = self
