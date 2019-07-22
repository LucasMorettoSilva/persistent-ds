from src.abc.version_tree import VersionTree


class QueueTP(VersionTree):

    def __init__(self):
        super().__init__()
        root = self._Leaf()
        self._entry.append(self._Entry(
            [root, root], 0
        ))

    def first(self, version=None):
        version = self._check_version(version)
        return self._entry[version][0].value

    def __enqueue(self, value, deque):
        u = self._Leaf(deque[0], value)
        self._add_leaf(u)
        if deque[0] is self.root:
            return u, u
        else:
            return u, deque[1]

    def enqueue(self, value, version=None):
        if value is None:
            raise ValueError("Invalid argument 'value' of None Type")
        version = self._check_version(version)

        first_last = self.__swap(self._entry[version].pointers)
        first_last = self.__swap(self.__enqueue(value, first_last))
        size  = self._entry[version].size + 1

        self._entry.append(self._Entry(first_last, size))

    def dequeue(self, version=None):
        version = self._check_version(version)

        first_last = self.__dequeue(self._entry[version].pointers)
        size  = self._entry[version].size - 1
        if size < 0:
            size = 0
        self._entry.append(self._Entry(first_last, size))
        return self._entry[version][0].value

    def __dequeue(self, first_last):
        first = first_last[0]
        last  = first_last[1]
        if first is last:
            return self.root, self.root
        elif self._lca(first, last) is first:
            la = self._la(last.depth - first.depth - 1, last)
            return la, last
        else:
            return first.parent, last

    def kth(self, k, version=None):
        version = self._check_version(version)

        if k <= 0 or k > self._entry[version].size:
            raise IndexError("K is out of bounds for given version")

        first_value = self._entry[version].pointers

        mid   = self._lca(first_value[0], first_value[1])
        l1    = first_value[0].depth - mid.depth
        l2    = first_value[1].depth - mid.depth

        if k - 1 <= l1:
            return self._la(k - 1, first_value[0]).value
        return self._la(l1 + l2 + 1 - k, first_value[1]).value

    def print(self, version=None):
        version = self._check_version(version)
        res = list()

        cur = self._entry[version][1]
        while cur.value:
            res.insert(0, cur.value)
            cur = cur.parent
        return str(res)

    @staticmethod
    def __swap(a):
        return a[1], a[0]
