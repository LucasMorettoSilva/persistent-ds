from abc import ABC

from collections.abc import Iterable


class VersionTree(ABC):

    class _Entry:

        def __init__(self, pts, size, last=None):
            if isinstance(pts, Iterable):
                self.__pts = pts
            else:
                self.__pts = [pts]
            self.__size = size
            self.last = last

        @property
        def pointers(self):
            return self.__pts

        @property
        def size(self):
            return self.__size

        def __getitem__(self, item):
            return self.__pts[item]

    class _Leaf:

        def __init__(self, parent=None, value=None):
            if parent is None:
                self.parent = self
                self.depth = 0
            else:
                self.parent = parent
                self.depth = self.parent.depth + 1
            self.value = value
            self.jump = self

    def __init__(self):
        self._entry = list()

    def size(self, version=None):
        version = self._check_version(version)
        return self._entry[version].size

    @property
    def root(self):
        return self._entry[0][0]

    @staticmethod
    def _la(k, u):
        y = u.depth - k
        while u.depth != y:
            if u.jump.depth >= y:
                u = u.jump
            else:
                u = u.parent
        return u

    @staticmethod
    def _lca(u, v):
        if u.depth > v.depth:
            u, v = v, u
        v = VersionTree._la(v.depth - u.depth, v)
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

    def _add_leaf(self, u):
        v = u.parent
        if v.jump is not self.root and \
           v.depth - v.jump.depth == v.jump.depth - v.jump.jump.depth:
            u.jump = v.jump.jump
        else:
            u.jump = v

    def _check_version(self, version):
        if version is not None:
            if version < 0 or version >= len(self._entry):
                raise ValueError("Invalid 'version': {}".format(version))

        if version is None:
            return len(self._entry) - 1
        return version
