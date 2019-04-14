#!usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'qaqmander'


class GF2Object_n:

    def __init__(self, _poly):
        self.poly = _poly

    def __add__(self, other):
        return GF2Object_n(self.poly ^ other.poly)

    def __sub__(self, other):
        return self + other

    def __mul__(self, other):
        return GF2Object_n(self.poly * other.poly)

    def __truediv__(self, other):
        if other == GF2Object_n(0):
            print('Error : GF2Object.__div__ -- other should not be ZERO')
            exit(-1)
        return self * GF2Object_n(1)

    def copy(self):
        return GF2Object_n(self.poly)

    def __eq__(self, other):
        return self.poly == other.poly

    def __str__(self):
        return '{}'.format(self.poly.__str__())

    def __repr__(self):
        return self.__str__()


class Polynomial_n:

    def __init__(self, _class, _ls):
        self._class = _class
        self.ls = _ls.copy()
        self.degree = len(self.ls) - 1
        zero = self._class(0)
        while self.ls[self.degree] == zero and self.degree > 0:
            self.ls.pop()
            self.degree -= 1

    @staticmethod
    def from_ls(_class, ls):
        ret_ls = list(map(lambda x: _class(x), ls))
        ret_ls.reverse()
        return Polynomial_n(_class, ret_ls)

    def __add__(self, other):
        max_deg = max(self.degree, other.degree)
        ret_ls = []
        for i in range(max_deg + 1):
            if i > self.degree:
                ret_ls.append(other.ls[i])
            elif i > other.degree:
                ret_ls.append(self.ls[i])
            else:
                ret_ls.append(self.ls[i] + other.ls[i])
        return Polynomial_n(self._class, ret_ls)

    def __sub__(self, other):
        max_deg = max(self.degree, other.degree)
        ret_ls = []
        for i in range(max_deg + 1):
            if i > self.degree:
                ret_ls.append(self._class(0) - other.ls[i])
            elif i > other.degree:
                ret_ls.append(self.ls[i])
            else:
                ret_ls.append(self.ls[i] - other.ls[i])
        return Polynomial_n(self._class, ret_ls)

    def __mul__(self, other):
        ret_ls = [self._class(0) for i in range(self.degree + other.degree + 1)]
        for i in range(self.degree + 1):
            for j in range(other.degree + 1):
                ret_ls[i + j] += self.ls[i] * other.ls[j]
        # print(ret_ls)
        return Polynomial_n(self._class, ret_ls)

    def __truediv__(self, other):
        if other.__class__ == self._class:
            ret_ls = []
            for i in self.ls:
                ret_ls.append(i / other)
            return Polynomial_n(self._class, ret_ls)
        else:
            print('Error : Polynomial.__truediv__ -- other.__class__ must be equal to self._class')
            exit(-1)

    def __divmod__(self, other):
        if self.degree < other.degree:
            return Polynomial_n(self._class, [self._class(0)]), self.copy()
        else:
            degree = self.degree - other.degree
            q = [self._class(0) for i in range(degree + 1)]
            r = self
            for i in range(degree + 1, -1, -1):
                if r.degree == other.degree + i:
                    q[i] = r.ls[-1] / other.ls[-1]
                    r = self - Polynomial_n(self._class, q) * other
            return Polynomial_n(self._class, q), r

    def gcd(self, other):
        # print(self, other)
        x1, y1 = Polynomial_n.from_ls(self._class, [1]), Polynomial_n.from_ls(self._class, [0])
        x2, y2 = Polynomial_n.from_ls(self._class, [0]), Polynomial_n.from_ls(self._class, [1])
        a, b = self, other
        zero = Polynomial_n.from_ls(self._class, [0])
        while b != zero:
            q, r = a.__divmod__(b)
            a, b = b, r
            x1, y1, x2, y2 = x2, y2, x1 - q * x2, y1 - q * y2
        return x1, y1, a

    def __eq__(self, other):
        if self.degree != other.degree:
            return False
        for i in range(self.degree + 1):
            if self.ls[i] != other.ls[i]:
                return False
        return True

    def copy(self):
        ret_ls = []
        for i in self.ls:
            ret_ls.append(i.copy())
        return Polynomial_n(self._class, ret_ls)

    def __str__(self):
        ls_r = self.ls.copy()
        ls_r.reverse()
        return 'Polynomial( {} )'.format(' '.join(map(self._class.__str__, ls_r)))

    def __repr__(self):
        return self.__str__()


class GF24Object_n:

    _irre_poly = Polynomial_n.from_ls(GF2Object_n, [1, 1, 0, 0, 1])

    def __init__(self, _ls):
        if _ls.__class__ == int:
            if _ls == 1:
                self.poly = Polynomial_n.from_ls(GF2Object_n, [1])
            elif _ls == 0:
                self.poly = Polynomial_n.from_ls(GF2Object_n, [0])
        elif _ls.__class__ == Polynomial_n:
            _, self.poly = _ls.__divmod__(GF24Object_n._irre_poly)
        else:
            _, self.poly = Polynomial_n(GF2Object_n, _ls).__divmod__(GF24Object_n._irre_poly)

    @staticmethod
    def from_ls(ls):
        return GF24Object_n(Polynomial_n.from_ls(GF2Object_n, ls))

    def __add__(self, other):
        return GF24Object_n(self.poly + other.poly)

    def __sub__(self, other):
        return GF24Object_n(self.poly - other.poly)

    def __mul__(self, other):
        return GF24Object_n(self.poly * other.poly)

    def inv(self):
        ret, _, _ = Polynomial_n.gcd(self.poly, GF24Object_n._irre_poly)
        return GF24Object_n(ret)

    def __truediv__(self, other):
        return self * other.inv()

    def __eq__(self, other):
        return self.poly == other.poly

    def copy(self):
        return GF24Object_n(self.poly.copy())

    def __str__(self):
        return 'GF24Object({})'.format(self.poly.__str__()[11:-1])

    def __repr__(self):
        return self.__str__()


class GF28Object_n:

    _irre_poly = Polynomial_n(GF24Object_n, [GF24Object_n.from_ls([1, 0]),
                                             GF24Object_n.from_ls([1]),
                                             GF24Object_n.from_ls([1])])

    def __init__(self, _ls):
        if _ls.__class__ == Polynomial_n:
            _, self.poly = _ls.__divmod__(GF28Object_n._irre_poly)
        else:
            _, self.poly = Polynomial_n(GF24Object_n, _ls).__divmod__(GF28Object_n._irre_poly)

    def get(self, index):
        if index == 0:
            return self.poly[0]
        elif index == 1:
            if len(self.poly) > 1:
                return self.poly[1]
            else:
                return GF24Object_n.from_ls([0])

    @staticmethod
    def from_ls(_ls):
        ls = [0] * (8 - len(_ls)) + _ls
        return GF28Object_n([GF24Object_n.from_ls(ls[4:]), GF24Object_n.from_ls(ls[:4])])

    def __add__(self, other):
        return GF28Object_n(self.poly + other.poly)

    def __sub__(self, other):
        return GF28Object_n(self.poly - other.poly)

    def __mul__(self, other):
        return GF28Object_n(self.poly * other.poly)

    def inv(self):
        x, _, d = Polynomial_n.gcd(self.poly, GF28Object_n._irre_poly)
        return GF28Object_n(x / d.ls[0])

    def __truediv__(self, other):
        return GF28Object_n(self * other.inv())

    def __eq__(self, other):
        return self.poly == other.poly

    def copy(self):
        return GF28Object_n(self.poly.copy())

    def __str__(self):
        return 'GF28Object({})'.format(self.poly.__str__()[11:-1])

    def __repr__(self):
        return self.__str__()

    def to_bin_list(self):
        ls = self.poly.ls
        ls_low = ls[0].poly.ls.copy()
        ls_low.reverse()
        ls_high = [0, 0, 0, 0] if len(ls) == 1 else ls[1].poly.ls.copy()
        ls_high.reverse()
        s = ''.join(map(str, ls_high)).rjust(4, '0') + ''.join(map(str, ls_low)).rjust(4, '0')
        return list(map(int, s))


one = GF28Object_n([GF24Object_n.from_ls([1])])
zero = GF28Object_n([GF24Object_n.from_ls([0])])


def find_generator():
    ret_ls = []
    for i in range(1 << 4):
        print(i)
        a = GF24Object_n.from_ls(list(map(int, bin(i)[2:])))
        for j in range(1 << 4):
            b = GF24Object_n.from_ls(list(map(int, bin(j)[2:])))
            x = GF28Object_n([b, a])
            if x == zero:
                continue
            now = x
            tot = 1
            while now != one:
                tot += 1
                now *= x
            if tot == 255:
                ret_ls.append(x)
    return ret_ls


if __name__ == '__main__':
    import pickle

    ls = find_generator()
    # ls = find_generator()
    with open('pr242', 'wb') as f:
        pickle.dump(ls, f)
    for i in ls:
        print(i)
    exit(0)

    x = ls[0]
    now = one
    with open('a.txt', 'w') as fw:
        for i in range(255):
            print(now.to_bin_list())
            print(now)
            now *= x

