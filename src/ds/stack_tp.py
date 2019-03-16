from src.util.numbers import Numbers


class StackTP:

    class __Leaf:

        def __init__(self, node=None, parent=None, depth=0):
            self.node      = node
            self.parent    = parent
            self.depth     = depth
            self.jump      = self
            self.node.leaf = self

    class __Node:

        def __init__(self, val=None, next=None, size=0, leaf=None):
            self.val  = val
            self.next = next
            self.size = size
            self.leaf = leaf

    def __init__(self):
        self.__version = list()
        self.__root           = self.__Leaf(self.__Node())
        self.__root.parent    = self.__root
        self.__root.node.leaf = self.__root
        self.__version.append(self.__root.node)

    @staticmethod
    def __level_ancestor(k, u):
        y = u.depth - k
        while u.depth != y:
            if u.jump.depth >= y:
                u = u.jump
            else:
                u = u.parent
        return u

    @staticmethod
    def __lca(u, v):
        if u.depth > v.depth:
            u, v = v, u
        v = StackTP.__level_ancestor(v.depth - u.depth, v)
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

    def __add_leaf(self, u):
        v = u.parent
        if v.jump is not self.__root and \
           v.depth - v.jump.depth == v.jump.depth - v.jump.jump.depth:
            u.jump = v.jump.jump
        else:
            u.jump = v

    def kth(self, k, version=None):
        if k <= 0:
            raise IndexError("K is out of bounds for given version")

        if version is None:
            version = len(self.__version) - 1
        if k > self.__version[version].size:
            raise IndexError("K is out of bounds for given version")

        return self.__level_ancestor(
            self.__version[version].size - k,
            self.__version[version].leaf
        ).node.val

    def size(self, version=None):
        if version is None:
            return self.__version[-1].size
        return self.__version[version].size

    def top(self, version=None):
        if version is None:
            return self.__version[-1].val
        return self.__version[version].val

    def pop(self, version=None):
        if version is None:
            version = len(self.__version) - 1
        if self.__version[version].val is None:
            return None
        self.__version.append(self.__version[version].next)
        return self.__version[version].val

    def push(self, val, version=None):
        if version is None:
            version = len(self.__version) - 1
        next = self.__version[version]
        node = self.__Node(val, next, next.size + 1)
        leaf = self.__Leaf(node, next.leaf, next.leaf.depth + 1)
        j = leaf.depth - (2 ** Numbers.non_zero(Numbers.skew_binary(leaf.depth))) + 1
        leaf.jump = self.__version[j].leaf
        self.__version.append(node)
        # self.__add_leaf(leaf)



