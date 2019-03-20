from abc import abstractmethod


class VersionTree:

    class :

    def __init__(self, root):
        self.__root = root

    @abstractmethod
    def create_leaf(self):

    @property
    def root(self):
        return self.__root

    @staticmethod
    def la(k, u):
        y = u.depth - k
        while u.depth != y:
            if u.jump.depth >= y:
                u = u.jump
            else:
                u = u.parent
        return u

    @staticmethod
    def lca(u, v):
        if u.depth > v.depth:
            u, v = v, u
        v = VersionTree.la(v.depth - u.depth, v)
        if v is u:
            return u
        while u.parent is not v.parent:
            if u.jump is not v.jump:
                u = u.jump
                v = v.jump
            else:
                u = u.parent
                v = v.parent
        return u.parent

    def add_leaf(self, u):
        v = u.parent
        if v.jump is not self.__root and \
           v.depth - v.jump.depth == v.jump.depth - v.jump.jump.depth:
            u.jump = v.jump.jump
        else:
            u.jump = v
