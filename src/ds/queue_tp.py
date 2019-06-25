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

        deque = self.__swap(self._entry[version].pointers)
        deque = self.__swap(self.__enqueue(value, deque))
        size  = self._entry[version].size + 1

        self._entry.append(self._Entry(deque, size))

    def dequeue(self, version=None):
        version = self._check_version(version)

        deque = self.__dequeue(self._entry[version].pointers)
        size  = self._entry[version].size - 1
        if size < 0:
            size = 0
        self._entry.append(self._Entry(deque, size))
        return self._entry[version][0].value

    def __dequeue(self, deque):
        first = deque[0]
        last  = deque[1]
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

        deque = self._entry[version].pointers

        mid   = self._lca(deque[0], deque[1])
        l1    = deque[0].depth - mid.depth
        l2    = deque[1].depth - mid.depth

        if k - 1 <= l1:
            return self._la(k - 1, deque[0]).value
        return self._la(l1 + l2 + 1 - k, deque[1]).value

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
