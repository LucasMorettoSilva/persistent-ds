class DequeTP:

    class __Node:

        def __init__(self, val=None, parent=None, depth=0):
            self.val    = val
            self.parent = parent
            self.depth  = depth
            self.jump   = self


    def __init__(self):
        self.__version = list()
        self.__root           = self.__Node()
        self.__root.parent    = self.__root
        self.__version.append(((
            self.__root,
            self.__root), 0
        ))

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
        v = DequeTP.__level_ancestor(v.depth - u.depth, v)
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

    def __check_version(self, version):
        if version is not None:
            if version < 0 or version >= len(self.__version):
                raise ValueError("Invalid 'version': {}".format(version))

        if version is None:
            return len(self.__version) - 1
        return version

    def front(self, version=None):
        version = self.__check_version(version)
        return self.__version[version][0][0].val

    def back(self, version=None):
        version = self.__check_version(version)
        return self.__version[version][0][1].val

    def push_front(self, val, version=None):
        if val is None:
            raise ValueError("Invalid argument 'val' of None Type")
        version = self.__check_version(version)
        deque = self.__push_front(val, self.__version[version][0])
        size  = self.__version[version][1] + 1
        self.__version.append((deque, size))

    def __push_front(self, val, deque):
        if deque[0].val is None:
            u = self.__Node(val, self.__root, 1)
            self.__add_leaf(u)
            return u, u
        else:
            u = self.__Node(val, deque[0], deque[0].depth + 1)
            self.__add_leaf(u)
            return u, deque[1]

    def push_back(self, val, version=None):
        if val is None:
            raise ValueError("Invalid argument 'val' of None Type")
        version = self.__check_version(version)
        deque   = self.__swap(self.__version[version][0])
        size    = self.__version[version][1] + 1
        self.__version.append((
            self.__swap(self.__push_front(val, deque)),
            size
        ))

    def pop_front(self, version=None):
        version = self.__check_version(version)
        deque = self.__pop_front(self.__version[version][0])
        size  = self.__version[version][1] - 1
        if size < 0:
            size = 0
        self.__version.append((deque, size))
        return self.__version[version][0][0].val

    def __pop_front(self, deque):
        first = deque[0]
        last  = deque[1]
        if first is last:
            return self.__root, self.__root
        elif self.__lca(first, last) is first:
            la = self.__level_ancestor(last.depth - first.depth - 1, last)
            return la, last
        else:
            return first.parent, last

    def pop_back(self, version=None):
        version = self.__check_version(version)
        deque = self.__swap(self.__version[version][0])
        size = self.__version[version][1] - 1
        if size < 0:
            size = 0
        self.__version.append((self.__swap(self.__pop_front(deque)), size))
        return deque[0].val

    def kth(self, k, version=None):
        if k <= 0:
            raise IndexError("K is out of bounds for given version")

        version = self.__check_version(version)

        if k > self.__version[version][1]:
            raise IndexError("K is out of bounds for given version")

        deque = self.__version[version][0]
        mid = self.__lca(deque[0], deque[1])
        l1  = deque[0].depth - mid.depth
        l2  = deque[1].depth - mid.depth
        if k - 1 <= l1:
            return self.__level_ancestor(k - 1, deque[0]).val
        return self.__level_ancestor(l1 + l2 + 1 - k, deque[1]).val

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
        return self.__version[version][1]

    @staticmethod
    def __swap(a):
        return a[1], a[0]



