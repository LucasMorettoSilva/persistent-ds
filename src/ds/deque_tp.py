from src.abc.leaf         import Leaf
from src.abc.version_tree import VersionTree


class DequeTP:

    class __AccessPoint:

        def __init__(self, first, last, size):
            self.first = first
            self.last  = last
            self.size  = size

        @property
        def access(self):
            return self.first, self.last

    class __Node(Leaf):

        def __init__(self, value=None, parent=None):
            super().__init__(parent, value)

    def __init__(self):
        self.__tree = VersionTree(self.__Node())
        self.__acs = list()
        self.__acs.append(
            self.__AccessPoint(
                self.__tree.root,
                self.__tree.root,
                0
            )
        )

    def __check_version(self, version):
        if version is not None:
            if version < 0 or version >= len(self.__acs):
                raise ValueError("Invalid 'version': {}".format(version))

        if version is None:
            return len(self.__acs) - 1
        return version

    def front(self, version=None):
        version = self.__check_version(version)
        return self.__acs[version].first.value

    def back(self, version=None):
        version = self.__check_version(version)
        return self.__acs[version].last.value

    def push_front(self, value, version=None):
        if value is None:
            raise ValueError("Invalid argument 'value' of None Type")
        version = self.__check_version(version)
        deque = self.__push_front(value, self.__acs[version].access)
        size  = self.__acs[version].size + 1
        self.__acs.append(self.__AccessPoint(deque[0], deque[1], size))

    def __push_front(self, value, deque):
        if deque[0].value is None:
            u = self.__Node(value, self.__tree.root)
            self.__tree.add_leaf(u)
            return u, u
        else:
            u = self.__Node(value, deque[0])
            self.__tree.add_leaf(u)
            return u, deque[1]

    def push_back(self, value, version=None):
        if value is None:
            raise ValueError("Invalid argument 'value' of None Type")
        version = self.__check_version(version)
        deque   = self.__swap(self.__acs[version].access)
        size    = self.__acs[version].size + 1
        deque   = self.__swap(self.__push_front(value, deque))
        self.__acs.append(self.__AccessPoint(deque[0], deque[1], size))

    def pop_front(self, version=None):
        version = self.__check_version(version)
        deque = self.__pop_front(self.__acs[version].access)
        size  = self.__acs[version].size - 1
        if size < 0:
            size = 0
        self.__acs.append(self.__AccessPoint(deque[0], deque[1], size))
        return self.__acs[version].first.value

    def __pop_front(self, deque):
        first = deque[0]
        last  = deque[1]
        if first is last:
            return self.__tree.root, self.__tree.root
        elif self.__tree.lca(first, last) is first:
            la = self.__tree.la(last.depth - first.depth - 1, last)
            return la, last
        else:
            return first.parent, last

    def pop_back(self, version=None):
        version = self.__check_version(version)
        deque = self.__swap(self.__acs[version].access)
        size = self.__acs[version].size - 1
        if size < 0:
            size = 0
        deque = self.__swap(self.__pop_front(deque))
        self.__acs.append(self.__AccessPoint(deque[0], deque[1], size))
        return self.__acs[version].last.value

    def kth(self, k, version=None):
        if k <= 0:
            raise IndexError("K is out of bounds for given version")

        version = self.__check_version(version)

        if k > self.__acs[version].size:
            raise IndexError("K is out of bounds for given version")

        deque = self.__acs[version].access
        mid = self.__tree.lca(deque[0], deque[1])
        l1  = deque[0].depth - mid.depth
        l2  = deque[1].depth - mid.depth
        if k - 1 <= l1:
            return self.__tree.la(k - 1, deque[0]).value
        return self.__tree.la(l1 + l2 + 1 - k, deque[1]).value

    def print(self, version=None):
        version = self.__check_version(version)
        res = "[]"

        first = True
        for i in range(0, self.size(version)):
            current = self.kth(i + 1, version)
            if first:
                res = res.replace("]", "{}]".format(current))
                first = False
            else:
                res = res.replace("]", ", {}]".format(current))
        return res

    def size(self, version=None):
        version = self.__check_version(version)
        return self.__acs[version].size

    @staticmethod
    def __swap(a):
        return a[1], a[0]



