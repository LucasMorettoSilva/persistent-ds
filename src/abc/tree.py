from abc import ABC

from src.util.numbers import Numbers


class Tree(ABC):

    class __Node:

        def __init__(self, key=None, parent=None, depth=0):
            self.parent = parent
            self.depth  = depth
            self.key    = key
            self.jump   = self.__jump_pointer(key)

        @staticmethod
        def __jump_pointer(key):
            return key - (2 ** Numbers.non_zero(Numbers.skew_binary(key))) + 1


    def __init__(self):
        self.__root = self.__Node()









