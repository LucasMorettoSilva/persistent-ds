from abc import ABC


class Tree(ABC):

    class __Node:

        def __init__(self, parent, depth, key):
            self.parent = parent
            self.depth  = depth
            self.key    = key
            self.jump   =



