from src.abc.version_tree import VersionTree


class DequeTP(VersionTree):

    def __init__(self):
        super().__init__()
        root = self._Leaf()
        self._acs.append(self._AccessPoint(
            [root, root], 0
        ))

    def front(self, version=None):
        version = self._check_version(version)
        return self._acs[version][0].value

    def back(self, version=None):
        version = self._check_version(version)
        return self._acs[version][1].value

    def push_front(self, value, version=None):
        if value is None:
            raise ValueError("Invalid argument 'value' of None Type")
        version = self._check_version(version)

        deque = self.__push_front(value, self._acs[version].pointers)
        size  = self._acs[version].size + 1
        self._acs.append(self._AccessPoint(deque, size))

    def __push_front(self, value, deque):
        u = self._Leaf(deque[0], value)
        self._add_leaf(u)
        if deque[0] is self.root:
            return u, u
        else:
            return u, deque[1]

    def push_back(self, value, version=None):
        if value is None:
            raise ValueError("Invalid argument 'value' of None Type")
        version = self._check_version(version)

        deque = self.__swap(self._acs[version].pointers)
        deque = self.__swap(self.__push_front(value, deque))
        size  = self._acs[version].size + 1

        self._acs.append(self._AccessPoint(deque, size))

    def pop_front(self, version=None):
        version = self._check_version(version)

        deque = self.__pop_front(self._acs[version].pointers)
        size  = self._acs[version].size - 1
        if size < 0:
            size = 0
        self._acs.append(self._AccessPoint(deque, size))
        return self._acs[version][0].value

    def __pop_front(self, deque):
        first = deque[0]
        last  = deque[1]
        if first is last:
            return self.root, self.root
        elif self._lca(first, last) is first:
            la = self._la(last.depth - first.depth - 1, last)
            return la, last
        else:
            return first.parent, last

    def pop_back(self, version=None):
        version = self._check_version(version)

        deque = self.__swap(self._acs[version].pointers)
        deque = self.__swap(self.__pop_front(deque))
        size  = self._acs[version].size - 1
        if size < 0:
            size = 0

        self._acs.append(self._AccessPoint(deque, size))
        return self._acs[version][1].value

    def kth(self, k, version=None):
        version = self._check_version(version)

        if k <= 0 or k > self._acs[version].size:
            raise IndexError("K is out of bounds for given version")

        deque = self._acs[version].pointers

        mid   = self._lca(deque[0], deque[1])
        l1    = deque[0].depth - mid.depth
        l2    = deque[1].depth - mid.depth

        if k - 1 <= l1:
            return self._la(k - 1, deque[0]).value
        return self._la(l1 + l2 + 1 - k, deque[1]).value

    def print(self, version=None):
        version = self._check_version(version)
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

    @staticmethod
    def __swap(a):
        return a[1], a[0]
