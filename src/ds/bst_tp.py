class BSTTP:

    class __Node:

        def __init__(self, key, value, size):
            self.key   = key
            self.value = value
            self.size  = size
            self.left  = None
            self.right = None

    def __init__(self, cmp=None):
        self.__cmp   = cmp
        self.__entry = [None]

    def __copy(self, node):
        if node is None:
            return None
        cp = self.__Node(node.key, node.value, node.size)
        cp.left  = node.left
        cp.right = node.right
        return cp

    def __compare(self, a, b):
        if self.__cmp is not None:
            return self.__cmp(a, b)
        if a < b:
            return -1
        if a > b:
            return 1
        return 0

    def empty(self, version=None):
        return self.size(version) == 0

    @staticmethod
    def __size(x):
        if x is None:
            return 0
        return x.size

    def size(self, version=None):
        version = self.__check_version(version)
        return self.__size(self.__entry[version])

    def __check_version(self, version):
        if version is not None:
            if version < 0 or version >= len(self.__entry):
                raise ValueError("Invalid 'version': {}".format(version))
            return version
        return len(self.__entry) - 1

    def put(self, key, value, version=None):
        version = self.__check_version(version)

        if key is None:
            raise ValueError("Invalid argument 'key' of None Type")

        self.__entry.append(self.__put(self.__entry[version], key, value))

    def __put(self, x, key, value):
        if x is None:
            return self.__Node(key, value, 1)
        cmp   = self.__compare(key, x.key)
        clone = self.__copy(x)
        if   cmp < 0:
            clone.left = self.__put(clone.left, key, value)
        elif cmp > 0:
            clone.right = self.__put(clone.right, key, value)
        else:
            clone.value = value
        clone.size = 1 + self.__size(clone.left) + self.__size(clone.right)
        return clone

    def get(self, key, version=None):
        version = self.__check_version(version)

        if key is None:
            raise ValueError("Invalid argument 'key' of None Type")

        return self.__get(self.__entry[version], key)

    def __get(self, x, key):
        if x is None:
            return None
        cmp = self.__compare(key, x.key)
        if   cmp < 0:
            return self.__get(x.left, key)
        elif cmp > 0:
            return self.__get(x.right, key)
        return x.value

    def contains(self, key, version=None):
        return self.get(key, version) is not None

    def delete(self, key, version=None):
        version = self.__check_version(version)

        if key is None:
            raise ValueError("Invalid argument 'key' of None Type")

        if self.contains(key, version):
            self.__entry.append(self.__delete(self.__entry[version], key))

    def __delete(self, x, key):
        if x is None:
            return None
        cmp = self.__compare(key, x.key)
        clone = self.__copy(x)
        if cmp < 0:
            clone.left = self.__delete(clone.left, key)
        elif cmp > 0:
            clone.right = self.__delete(clone.right, key)
        else:
            if clone.right is None:
                return clone.left
            if clone.left  is None:
                return clone.right
            t = clone
            clone = self.__copy(self.__min(t.right))
            clone.right = self.__delete_min(t.right)
            clone.left  = t.left
        clone.size = 1 + self.__size(clone.left) + self.__size(clone.right)
        return clone

    def min(self, version=None):
        version = self.__check_version(version)

        if self.size(version) == 0:
            raise AttributeError("BST underflow, called min() with empty BST")

        return self.__min(self.__entry[version]).key

    def __min(self, x):
        if x.left is None:
            return x
        return self.__min(x.left)

    def max(self, version=None):
        version = self.__check_version(version)

        if self.size(version) == 0:
            raise AttributeError("BST underflow, called max() with empty BST")

        return self.__max(self.__entry[version]).key

    def __max(self, x):
        if x.right is None:
            return x
        return self.__max(x.right)

    def delete_min(self, version=None):
        version = self.__check_version(version)

        if self.size(version) == 0:
            raise AttributeError("BST underflow, called delete_min() with empty BST")

        self.__entry.append(self.__delete_min(self.__entry[version]))

    def __delete_min(self, x):
        clone = self.__copy(x)
        if clone.left is None:
            return self.__copy(clone.right)
        clone.left = self.__delete_min(clone.left)
        clone.size = 1 + self.__size(clone.left) + self.__size(clone.right)
        return clone

    def delete_max(self, version=None):
        version = self.__check_version(version)

        if self.size(version) == 0:
            raise AttributeError("BST underflow, called delete_max() with empty BST")

        self.__entry.append(self.__delete_max(self.__entry[version]))

    def __delete_max(self, x):
        clone = self.__copy(x)
        if clone.right is None:
            return self.__copy(clone.left)
        clone.right = self.__delete_max(clone.right)
        clone.size = 1 + self.__size(clone.left) + self.__size(clone.right)
        return clone

    def keys_in_order(self, version=None):
        version = self.__check_version(version)

        keys  = []
        stack = []
        cur = self.__entry[version]
        while cur is not None or len(stack) > 0:
            while cur is not None:
                stack.append(cur)
                cur = cur.left
            cur = stack.pop()
            keys.append(cur.key)
            cur = cur.right
        return keys
