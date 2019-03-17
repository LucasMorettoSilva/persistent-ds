from src.abc.leaf         import Leaf
from src.abc.version_tree import VersionTree


class StackTP:

    class __Node(Leaf):

        def __init__(self, value=None, parent=None, size=0):
            super().__init__(parent, value)
            self.size = size

    def __init__(self):
        self.__tree = VersionTree(self.__Node())
        self.__acs  = [self.__tree.root]

    def kth(self, k, version=None):
        version = self.__check_version(version)

        if k <= 0 or k > self.__acs[version].size:
            raise IndexError("K is out of bounds for given version")

        return self.__tree.la(
            self.__acs[version].size - k,
            self.__acs[version]
        ).value

    def size(self, version=None):
        version = self.__check_version(version)
        return self.__acs[version].size

    def top(self, version=None):
        version = self.__check_version(version)
        return self.__acs[version].value

    def pop(self, version=None):
        version = self.__check_version(version)
        if self.__acs[version].value is None:
            return None
        self.__acs.append(self.__acs[version].parent)
        return self.__acs[version].value

    def push(self, value, version=None):
        if value is None:
            raise ValueError("Invalid argument 'value' of None Type")
        version = self.__check_version(version)

        nxt  = self.__acs[version]
        node = self.__Node(value, nxt, nxt.size + 1)
        self.__tree.add_leaf(node)
        self.__acs.append(node)

    def print(self, version=None):
        version = self.__check_version(version)

        res   = "[]"
        first = True
        curr  = self.__acs[version]
        while curr.value is not None:
            if first:
                res = res.replace("]", "{}]".format(curr.value))
                first = False
            else:
                res = res.replace("]", ", {}]".format(curr.value))
            curr = curr.parent
        return res

    def __check_version(self, version):
        if version is not None:
            if version < 0 or version >= len(self.__acs):
                raise ValueError("Invalid 'version': {}".format(version))

        if version is None:
            return len(self.__acs) - 1
        return version
