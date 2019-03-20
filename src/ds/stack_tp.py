from src.abc.version_tree import VersionTree


class StackTP(VersionTree):

    def __init__(self):
        super().__init__()
        self._acs.append(self._AccessPoint(self._Leaf(), 0))

    def kth(self, k, version=None):
        version = self._check_version(version)

        if k <= 0 or k > self._acs[version].size:
            raise IndexError("K is out of bounds for given version")

        return self._la(
            self._acs[version].size - k,
            self._acs[version][0]
        ).value


    def top(self, version=None):
        version = self._check_version(version)
        return self._acs[version][0].value

    def pop(self, version=None):
        version = self._check_version(version)

        if self._acs[version][0].value is None:
            return None

        self._acs.append(self._AccessPoint(
            self._acs[version][0].parent,
            self._acs[version].size - 1)
        )
        return self._acs[version][0].value

    def push(self, value, version=None):
        if value is None:
            raise ValueError("Invalid argument 'value' of None Type")
        version = self._check_version(version)

        nxt  = self._acs[version]
        leaf = self._Leaf(nxt[0], value)
        self._add_leaf(leaf)
        self._acs.append(self._AccessPoint(leaf, nxt.size + 1))

    def print(self, version=None):
        version = self._check_version(version)

        res   = "[]"
        first = True
        curr  = self._acs[version][0]
        while curr.value is not None:
            if first:
                res = res.replace("]", "{}]".format(curr.value))
                first = False
            else:
                res = res.replace("]", ", {}]".format(curr.value))
            curr = curr.parent
        return res
