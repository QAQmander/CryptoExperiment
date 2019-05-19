# -*- coding: utf-8 -*-

from src.ECC.PFiniteField import PObject, ZERO, ONE


class EccPoint(object):
    a = PObject(0xBB8E5E8FBC115E139FE6A814FE48AAA6F0ADA1AA5DF91985)
    b = PObject(0x1854BEBDC31B21B7AEFC80AB0ECD10D5B1B3308E6DBF11C1)

    def __init__(self, x, y, z):
        assert (x.__class__ == y.__class__ == z.__class__ == PObject)
        self.x = x
        self.y = y
        self.z = z

    def check(self):
        if self.z == ZERO:
            return True
        return self.x * self.x * self.x + \
               EccPoint.a * self.x + \
               EccPoint.b == self.y * self.y

    @staticmethod
    def set_a_b(a, b):
        EccPoint.a = PObject(a).copy()
        EccPoint.b = PObject(b).copy()

    def get_x(self):
        return self.x.get_num()

    def get_y(self):
        return self.y.get_num()

    def get_z(self):
        return self.z.get_num()

    def __add__(self, other):
        assert (other.__class__ == EccPoint)
        if self.z == ZERO:
            return other.copy()
        elif other.z == ZERO:
            return self.copy()
        elif self.y == - other.y:
            return EccPoint(ONE, ONE, ZERO)
        elif self == other:
            delta = ((self.x * self.x * 3 + EccPoint.a) / (self.y * 2))
            x = delta * delta - self.x * 2
            y = delta * (self.x - x) - self.y
            return EccPoint(x, y, ONE)
        else:
            delta = (other.y - self.y) / (other.x - self.x)
            x = delta * delta - self.x - other.x
            y = delta * (self.x - x) - self.y
            return EccPoint(x, y, ONE)

    def __neg__(self):
        return EccPoint(self.x, self.y, -self.z)

    def __sub__(self, other):
        assert (other.__class__ == EccPoint)
        return self + (- other)

    def __mul__(self, other):
        assert (other.__class__ == int)
        n = other
        x = self.copy()
        ans = EccPoint(ONE, ONE, ZERO)
        while n:
            if n & 1:
                ans = ans + x
                n -= 1
            else:
                x = x + x
                n >>= 1
        return ans

    def __eq__(self, other):
        assert (other.__class__ == EccPoint)
        flag = True
        flag &= self.x == other.x
        flag &= self.y == other.y
        flag &= self.z == other.z
        return flag

    def copy(self):
        return EccPoint(self.x, self.y, self.z)

    def __str__(self):
        return 'EccPoint:\n' + str(self.x) + '\n' + str(self.y) + '\n' + str(self.z)


INFINITE = EccPoint(ONE, ONE, ZERO)


if __name__ == '__main__':
    '''
    PObject.set_prime(23)
    EccPoint.set_a_b(1, 1)
    p = EccPoint(PObject(3), PObject(10), ONE)
    q = EccPoint(PObject(9), PObject(7), ONE)
    print(p.check())
    print(q.check())
    print(p + q)
    '''
    x = PObject(0x4AD5F7048DE709AD51236DE65E4D4B482C836DC6E4106640)
    y = PObject(0x02BB3A02D4AAADACAE24817A4CA3A1B014B5270432DB27D2)
    d = 0x58892B807074F53FBF67288A1DFAA1AC313455FE60355AFD
    p = EccPoint(x, y, PObject(1))
    print(p.check())
    q = p * d
    print(q.x)
    print(q.y)
    print(q.z)
