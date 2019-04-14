#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# base = 4  irre = 0b11001
# base = 8  irre = 0b100011011


class Polynomial2(object):  # GF2[x]

    def __init__(self, poly):
        self._poly = poly
        self._length = -1
        while poly:
            self._length += 1
            poly //= 2

    def copy(self):
        return Polynomial2(self._poly)

    def add(self, other):
        return Polynomial2(self._poly ^ other._poly)

    def sub(self, other):
        return self.add(other)

    def mul(self, other):
        ret = Polynomial2(0)
        for i in range(other._length + 1):
            if (other._poly >> i) & 1:
                ret = ret.add(Polynomial2(self._poly << i))
        return ret

    def eq(self, other):
        return self._poly == other._poly

    def biggerThan(self, other):
        return self._length > other._length

    def smallThan(self, other):
        return self._length < other._length

    def div(self, other):  # divide with remainder
        if other.eq(Polynomial2(0)):
            print('Error : FiniteField.Polynomial2.div -- div ZERO')
            return None
        r = self.copy()
        q = Polynomial2(0)
        while not r.smallThan(other):
            now = Polynomial2(1 << (r._length - other._length))
            q = q.add(now)
            r = r.sub(now.mul(other))
        return q, r

    @staticmethod
    def gcd(a, b):  # return x, y, d s.t. ax+by=d
        a, b = a.copy(), b.copy()
        x1, y1 = Polynomial2(1), Polynomial2(0)
        x2, y2 = Polynomial2(0), Polynomial2(1)
        zero = Polynomial2(0)
        while not b.eq(zero):
            q, r = a.div(b)
            x1, y1, x2, y2 = x2, y2, x1.sub(q.mul(x2)), y1.sub(q.mul(y2))
            a, b = b, r
        return x1, y1, a

    def __int__(self):
        return self._poly

    def __str__(self):
        return 'Polynomial2( {} )'.format(' '.join(list(bin(self._poly)[2:])))

    def __repr__(self):
        return self.__str__()


class GF24Object(object):  # factor in GF(2^4)

    _irre = Polynomial2(0b11001)

    def __init__(self, poly):
        if isinstance(poly, Polynomial2):
            self._poly = poly.div(GF24Object._irre)[1]
        elif isinstance(poly, int):
            self._poly = Polynomial2(poly).div(GF24Object._irre)[1]

    def add(self, other):
        return GF24Object(self._poly.add(other._poly))

    def sub(self, other):
        return GF24Object(self._poly.sub(other._poly))

    def mul(self, other):
        return GF24Object(self._poly.mul(other._poly))

    def eq(self, other):
        return self._poly.eq(other._poly)

    def inv(self):  # invert
        if self.eq(GF24Object(Polynomial2(0))):
            print('Error : FiniteField.GF24Object.inv -- require inv of ZERO')
            return None
        else:
            return GF24Object(self._poly.gcd(GF24Object._irre)[0])

    def div(self, other):
        return GF24Object(self._poly.mul(other.inv()))

    def __str__(self):
        return 'GF24Object( {} )'.format(self._poly.__str__())

    def __repr__(self):
        return self.__str__()


class GF28Object(object):  # GF(2^8)

    # _irre = Polynomial2(0b111111001)
    _irre = Polynomial2(0b100011011)

    def __init__(self, poly):
        if isinstance(poly, Polynomial2):
            self._poly = poly.div(GF28Object._irre)[1]
        elif isinstance(poly, int):
            self._poly = Polynomial2(poly).div(GF28Object._irre)[1]

    def add(self, other):
        return GF28Object(self._poly.add(other._poly))

    def sub(self, other):
        return GF28Object(self._poly.sub(other._poly))

    def mul(self, other):
        return GF28Object(self._poly.mul(other._poly))

    def eq(self, other):
        return self._poly.eq(other._poly)

    def inv(self):
        if self.eq(GF28Object(Polynomial2(0))):
            print('Error : GF28Object.inv -- require inv of ZERO')
            return None
        else:
            return GF28Object(self._poly.gcd(GF28Object._irre)[0])

    def div(self, other):
        return GF28Object(self._poly.mul(other.inv()))

    def __int__(self):
        return self._poly.__int__()

    def __str__(self):
        return 'GF28Object( {} )'.format(self._poly.__str__())

    def __repr__(self):
        return self.__str__()

    def to_bin_list(self):
        p = self._poly._poly
        return list(map(int, bin(p)[2:].rjust(8, '0')))


def find_generator_24():
    one = GF24Object(1)
    for i in range(1 << 4):
        if i == 0:
            continue
        x = GF24Object(i)
        now = GF24Object(i)
        tot = 1
        while not now.eq(one):
            tot += 1
            now = now.mul(x)
        if tot == 15:
            print(x, tot)
            now = one
            for j in range(14):
                now = now.mul(x)
            print(now)


def find_generator():
    ret_ls = []
    one = GF28Object(1)
    for i in range(1 << 8):
        print(i)
        if i == 0:
            continue
        x = GF28Object(i)
        now = GF28Object(i)
        tot = 1
        while not now.eq(one):
            tot += 1
            now = now.mul(x)
        if tot == 255:
            ret_ls.append(x)
    return ret_ls


if __name__ == '__main__':
    import pickle
    with open('pr28', 'rb') as fr:
        ls = pickle.load(fr)
    print(len(ls))
    exit(0)
    for i in ls:
        print(i)
        print(i.to_bin_list())
    exit(0)
    one_8 = GF28Object(1)
    now = one_8
    with open('b.txt', 'w') as fw:
        for i in range(256):
            s = bin(now._poly._poly)[2:].rjust(8, '0')
            print(s)
            fw.write(s + '\n')
            now = now.mul(x)
