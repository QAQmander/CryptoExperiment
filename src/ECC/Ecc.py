# -*- coding: utf-8 -*-

from src.ECC.PFiniteField import PObject, ZERO, ONE


class EccPoint(object):
    a = PObject(10)
    b = PObject(100)

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        if self == other:
            delta = (self.x * self.x * 3 + EccPoint.a / (self.y * 2))
            x = delta * delta - 2 * self.x
            y = delta * (self.x - x) - self.y
            return EccPoint(self.x, self.y, self.z)
        else:
            delta = (other.y - self.y) / (other.x - self.x)
            x = delta * delta - self.x - other.x
            y = - self.y + delta * (self.x - other.x)
            return EccPoint(self.x, self.y)

    def __eq__(self, other):
        flag = True
        flag &= self.x == other.x
        flag &= self.y == other.y
        flag &= self.z == other.z
        return flag
