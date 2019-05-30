# -*- coding: utf-8 -*-

from src.ECC.PFiniteField import PObject, ZERO, ONE
from src.ECC.Ecc import EccPoint, INFINITE
from src.sha3.sha3 import sha3_256 as _orig_sha3_256
from src.sha3.sha3 import wrapper
from struct import pack, unpack
from random import randint
from src.infrastructure.Euclid import inv

hash_func = wrapper(_orig_sha3_256)

COOR_LENGTH = 24
HASH_LENGTH = 256 // 8
P_LENGTH = 32


class SM2_DigitalSignal(object):

    def __init__(self, entl: int, id: bytes, g: EccPoint, pri: int) -> None:
        assert (entl.__class__ == int and 0 < entl < 65536)
        assert (id.__class__ == bytes)
        assert (g.__class__ == EccPoint)
        assert (pri.__class__ == int)
        self.g = g
        self.pri = pri
        self.pub = self.g * self.pri
        bentl = pack('H', entl)
        coor2bytes = SM2_DigitalSignal.coor2bytes
        ba = coor2bytes(EccPoint.a.get_num())
        bb = coor2bytes(EccPoint.b.get_num())
        assert (self.g != INFINITE)
        bgx, bgy = coor2bytes(self.g.get_x()), coor2bytes(self.g.get_y())
        assert (self.pub != INFINITE)
        bpx, bpy = coor2bytes(self.pub.get_x()), coor2bytes(self.pub.get_y())
        self.z = hash_func(bentl + id + ba + bb + bgx + bgy + bpx + bpy)

    @staticmethod
    def coor2bytes(x: int, width=COOR_LENGTH) -> bytes:
        ret = b''
        while x:
            ret = pack('B', x % 256) + ret
            x //= 256
        ret = ret.rjust(width, b'\x00')
        return ret

    @staticmethod
    def bytes2coor(x: bytes) -> int:
        ret = 0
        for i in x:
            ret = ret * 256 + i
        return ret

    def sign(self, message: bytes) -> bytes:
        m_ = self.z + message
        bytes2coor = SM2_DigitalSignal.bytes2coor
        coor2bytes = SM2_DigitalSignal.coor2bytes
        e = bytes2coor(hash_func(m_))
        while True:
            k = randint(1, n - 1)
            x1 = (self.g * k).get_x()
            r = (e + x1) % n
            if r == 0 or r + k == n:
                continue
            good = inv(1 + self.pri, n)
            s = good * (k - r * self.pri) % n
            if s == 0:
                continue
            break
        r = coor2bytes(r, P_LENGTH)
        s = coor2bytes(s, P_LENGTH)
        return r + s

    def check(self, z: bytes, message: bytes, sign: bytes) -> bool:
        bytes2coor = SM2_DigitalSignal.bytes2coor
        r = bytes2coor(sign[:P_LENGTH]) # type: int
        s = bytes2coor(sign[P_LENGTH:]) # type: int
        if not (1 <= r <= n - 1):
            return False
        if not (1 <= s <= n - 1):
            return False
        m_ = z + message
        e = bytes2coor(hash_func(m_))
        t = (r + s) % n
        if t == 0:
            return False
        x1 = (self.g * s + self.pub * t).get_x() # type: int
        R = (e + x1) % n
        if R != r:
            return False
        return True


p = 0x8542D69E4C044F18E8B92435BF6FF7DE457283915C45517D722EDB8B08F1DFC3
a = 0x787968B4FA32C3FD2417842E73BBFEFF2F3C848B6831D7E0EC65228B3937E498
b = 0x63E4C6D3B23B0C849CF84241484BFE48F61D59A5B16BA06E6E12D1DA27C5249A
gx = 0x421DEBD61B62EAB6746434EBC3CC315E32220B3BADD50BDC4C4E6C147FEDD43D
gy = 0x0680512BCBB42C07D47349D2153B70C4E5D7FDFCBFA36EA1A85841B9E46E09A2
d = 0x128B2FA8BD433C6C068C8D803DFF79792A519A55171B1B650C23661D15897263
n = 0x8542D69E4C044F18E8B92435BF6FF7DD297720630485628D5AE74EE7C32E79B7
entla = 0x0090
ida = 'ALICE123@YAHOO.COM'.encode('ascii')

if __name__ == '__main__':
    PObject.set_prime(p)
    EccPoint.set_a_b(a, b)
    g = EccPoint(PObject(gx), PObject(gy), ONE)
    a = SM2_DigitalSignal(entla, ida, g, d)
    message = b'message digest'
    sign = a.sign(message)
    print(a.check(a.z, message, sign))
