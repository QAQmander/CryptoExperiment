# -*- coding: utf-8 -*-

from src.infrastructure.Euclid import gcd_const


class PObject(object):
    p = 100000007

    def __init__(self, x):
        self.x = x % PObject.p
        if self.x < 0:
            self.x += PObject.p

    def __eq__(self, other):
        return self.x == other.x

    def __add__(self, other):
        return PObject(self.x + other.x)

    def __sub__(self, other):
        return PObject(self.x - other.x)

    def __mul__(self, other):
        assert(other.__class__ in (int, PObject))
        if other.__class__ == int:
            return PObject(self.x * other)
        else:
            return PObject(self.x * other.x)

    def __truediv__(self, other):
        return self * other.inv()

    def inv(self):
        return PObject(gcd_const(self.x, PObject.p)[0])

    def __str__(self):
        return self.x.__str__()

    def __repr__(self):
        return self.x.__repr__()


ZERO = PObject(0)

ONE = PObject(1)
