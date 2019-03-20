from abc import ABC


class AccessPoint(ABC):

    def __init__(self, pts, size):
        self.__pts  = pts
        self.__size = size

    @property
    def pointers(self):
        return self.__pts

    @property
    def size(self):
        return self.__size
