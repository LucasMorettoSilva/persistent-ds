class BSTPP:

    class __Node:

        def __init__(self, key=None):
            self.key    = key
            self.child  = [None, None]
            self.parent = None
            self.t = None
            self.copy = None
            self.extra = None
            self.extra_side = 0
            self.extra_t = -1
            self.red = True

    def __init__(self, cmp=None):
        self.__cmp   = cmp
        self.__entry = [None]
        self.__curr  = 0

    def __raw_copy(self, u):
        cp = self.__Node(u.key)
        cp.child  = u.child
        cp.parent = u.parent
        cp.red    = u.red
        return cp

    def __copy(self, u):
        cp = self.__raw_copy(u)
        cp.t = self.__curr
        if u.extra_t != -1:
            cp.child[u.extra_side] = u.extra
            cp.extra_t = -1
        if self.__entry[-1] is u:
            self.__entry[-1] = cp
        for side in range(2):
            if cp.child[side] is not None:
                cp.child[side].parent = cp
        u.parent = None
        if cp.parent is not None:
            v = cp.parent
            if self.__child(v, 1) is u:
                side = 1
            else:
                side = 0
            if v.t == self.__curr:
                v.child[side] = cp
            elif v.extra_t == -1:
                v.extra_t = self.__curr
                v.extra = cp
                v.extra_side = side
            else:
                v.copy = self.__copy(v)
                v.copy.child[side] = cp
                cp.parent = v.copy
        return cp

    def modify(self, u, side, v):
        u = self.__active(u)
        if u is None:
            return
        if u.t < self.__curr:
            u.copy = self.__copy(u)
            u = u.copy
        if u.child[side] is not None:
            u.child[side].parent = None
        u.child[side] = self.__active(v)
        if u.child[side] is not None:
            u.child[side].parent = u

    @staticmethod
    def __active(u):
        if u is None or u.copy is None:
            return u
        return u.copy

    def __child(self, u, side, version=None):
        if u is None:
            return None
        if version is None:
            return self.__child(self.__active(u), side, self.__curr)
        if u.extra_t != -1 and u.extra_side == side and version >= u.extra_t:
            return u.extra
        return u.child[side]

    def contains(self, key, version=None):
        version = self.__check_version(version)
        return self.__find(key, version) is not None

    def __find(self, key, version):
        u = self.__entry[version]
        while u is not None and key != u.key:
            u = self.__child(u, key > u.key, version)
        return u

    def insert(self, key):
        self.__curr += 1
        self.__entry.append(self.__entry[-1])
        x = self.__Node(key)
        x.t = self.__curr
        if self.__entry[-1] is None:
            self.__entry[-1] = x
        else:
            u = self.__entry[-1]
            v = None
            while u is not None:
                v = u
                u = self.__child(u, key > u.key)
            self.modify(v, key > v.key, x)
        while x.red and x.parent is not None and x.parent.red:
            y = x.parent
            z = y.parent
            sidex = self.__child(y, 1) is x
            sidey = self.__child(z, 1) is y
            w = self.__child(z, not sidey)
            if w is not None and w.red:
                z.red = True
                y.red = False
                w.red = False
                x = z
            else:
                if sidey != sidex:
                    self.__rotate(y, sidex)
                    x, y = y, x
                self.__rotate(z, sidey)
                if self.__active(z) is not None:
                    self.__active(z).red = True
                if self.__active(y) is not None:
                    self.__active(y).red = False
                break
        self.__entry[-1].red = False

    def __rotate(self, u, side):
        v = self.__child(u, side)
        b = self.__child(v, not side)
        self.modify(v, not side, None)
        self.modify(u, side, b)
        u = self.__active(u)
        if u is not None and u.parent is not None:
            self.modify(u.parent, self.__child(u.parent, 1) is u, v)
        else:
            self.__entry[-1] = self.__active(v)
        self.modify(v, not side, u)

    def __add_black(self, y, side):
        y = self.__active(y)
        while y is not None:
            z = self.__child(y, not side)
            if z.red:
                self.__swap_colors(y, z)
                self.__rotate(y, not side)
                y = self.__active(y)
                z = self.__child(y, not side)
            zx = self.__child(z, side)
            zz = self.__child(z, not side)
            if (zx is None or not zx.red) and (zz is None or not zz.red):
                z.red = True
                if y is self.__entry[-1] or y.red:
                    y.red = False
                    break
                else:
                    side = self.__child(y.parent, 1) is y
                    y = y.parent
            else:
                if zx is not None and zx.red:
                    self.__swap_colors(z, zx)
                    self.__rotate(z, side)
                    y = self.__active(y)
                    z = self.__child(y, not side)
                    zz = self.__child(z, not side)
                self.__swap_colors(y, z)
                zz.red = False
                self.__rotate(y, not side)
                break

    @staticmethod
    def __swap_colors(x, y):
        aux = x.red
        x.red = y.red
        y.red = aux

    def min(self, version=None):
        if version is None:
            version = self.__curr
        return self.__min(self.__entry[version]).key

    def max(self, version=None):
        if version is None:
            version = self.__curr
        return self.__max(self.__entry[version]).key

    def __max(self, u):
        while self.__child(u, 1) is not None:
            u = self.__child(u, 1)
        return u

    def __min(self, u):
        while self.__child(u, 0) is not None:
            u = self.__child(u, 0)
        return u

    def __transplant(self, u, x):
        x = self.__active(x)
        if x is not None and x.parent is not None:
            self.modify(x.parent, self.__child(x.parent, 1) is x, None)
        u = self.__active(u)
        v = u.parent
        if v is not None:
            self.modify(v, self.__child(v, 1) is u, x)
        else:
            self.__entry[-1] = x
        if x is not None:
            x.red = u.red

    def delete(self, key):
        self.__curr += 1
        self.__entry.append(self.__entry[-1])
        u = self.__find(key, self.__curr)
        v = u.parent
        if self.__child(u, 1) is None:
            need_fix = v is not None and not u.red and self.__child(u, 0) is None
            self.__transplant(u, self.__child(u, 0))
            if need_fix:
                self.__add_black(v, self.__child(v, 1) is None)
        else:
            x = self.__min(self.__child(u, 1))
            if x is self.__child(u, 1):
                y = x
            else:
                y = x.parent
            need_fix = not x.red and self.__child(x, 1) is None
            self.__transplant(x, self.__child(x, 1))
            self.__transplant(u, x)
            for side in range(2):
                child = self.__child(u, side)
                self.modify(u, side, None)
                self.modify(x, side, child)
            if need_fix:
                self.__add_black(y, self.__child(y, 1) is None)

    def __check_version(self, version):
        if version is not None:
            if version < 0 or version >= len(self.__entry):
                raise ValueError("Invalid 'version': {}".format(version))

        if version is None:
            return len(self.__entry) - 1
        return version

    def keys_in_order(self, version=None):
        v = self.__check_version(version)
        keys  = []
        stack = []
        cur   = self.__entry[v]
        while cur is not None or len(stack) > 0:
            while cur is not None:
                stack.append(cur)
                cur = self.__child(cur, 0, v)
            cur = stack.pop()
            keys.append(cur.key)
            cur = self.__child(cur, 1, v)
        return keys

    def print(self, version=None):
        keys = self.keys_in_order(version)
        return str(keys)





