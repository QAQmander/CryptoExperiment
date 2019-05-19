# -*- coding: utf-8 -*-

from src.infrastructure.Euclid import gcd_const


class PObject(object):
    p = 0xBDB6F4FE3E8B1D9E0DA8C0D46F4C318CEFE4AFE3B6B8551F

    def __init__(self, x):
        assert(x.__class__ == int)
        self.x = x % PObject.p
        if self.x < 0:
            self.x += PObject.p

    @staticmethod
    def set_prime(p):
        PObject.p = p

    def __eq__(self, other):
        assert (other.__class__ == PObject)
        return self.x == other.x

    def __add__(self, other):
        assert (other.__class__ == PObject)
        return PObject(self.x + other.x)

    def __sub__(self, other):
        assert (other.__class__ == PObject)
        return PObject(self.x - other.x)

    def __neg__(self):
        return PObject(- self.x)

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
        return hex(self.x)

    def __repr__(self):
        return hex(self.x)

    def copy(self):
        return PObject(self.x)

    def get_num(self):
        return self.x


ZERO = PObject(0)

ONE = PObject(1)
