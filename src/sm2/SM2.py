#!/usr/bin/env python3

import hashlib

from src.ECC.PFiniteField import PObject, ZERO, ONE
from src.ECC.Ecc import EccPoint, INFINITE
from random import randint

# hash_func: byte_str -> byte_str
def hash_func(bstr):
    s = hashlib.sha3_512()
    s.update(bstr)
    return s.digest()
# coordinate length in bytes
COOR_LENGTH = 24
C1_LENGTH = 1 + 2 * COOR_LENGTH
# output length of hash func in bytes
HASH_LENGTH = 512 // 8
C3_LENGTH = HASH_LENGTH


class SM2(object):

    def __init__(self, g, pri):
        assert (g.__class__ == EccPoint)
        assert (pri.__class__ == int)
        self.g = g
        self.pri = pri
        self.pub = self.g * self.pri

    @staticmethod
    def hex2barray(hex_str):
        assert(len(hex_str) % 2 == 0)
        ret = bytearray()
        for i in range(len(hex_str) // 2):
            ret.append(int(hex_str[2 * i: 2 * i + 2], 16))
        return ret

    @staticmethod
    def barray2hex(barray):
        ret = ''
        for i in range(len(barray)):
            ret += hex(barray[i])[2:].rjust(2, '0')
        return ret

    @staticmethod
    def eccpoint2str(p):
        assert (p.__class__ == EccPoint)
        assert (p != INFINITE)
        x_str = hex(p.get_x())[2:].rjust(2 * COOR_LENGTH, '0')
        y_str = hex(p.get_y())[2:].rjust(2 * COOR_LENGTH, '0')
        return x_str, y_str

    @staticmethod
    def barray2eccpoint(c1):
        x = int(SM2.barray2hex(c1[1: 1 + COOR_LENGTH]), 16)
        y = int(SM2.barray2hex(c1[1 + COOR_LENGTH:]), 16)
        return EccPoint(PObject(x), PObject(y), ONE)

    # plain: normal ascii str
    # ret value: byte array
    def encrypt(self, plain):
        k = randint(1, 256 ** COOR_LENGTH - 1)
        # print(k)
        p1 = self.g * k
        x1_str, y1_str = SM2.eccpoint2str(p1)
        pc = r'04'
        c1 = pc + x1_str + y1_str

        p2 = self.pub * k
        x2_str, y2_str = SM2.eccpoint2str(p2)
        t = SM2.kdf(x2_str + y2_str, len(plain) * 8)
        # for test
        # t1 = ['04', '6B', '04', 'A9', 'AD', 'F5', '3B', '38', '9B', '9E', '2A', 'AF', 'B4', '7D', '90',
        #       'F4', 'D0', '89', '78']
        # t = list(map(lambda x: int(x, 16), t1))
        bplain = plain.encode('ascii')
        c2 = bytearray()
        for i in range(len(bplain)):
            c2.append(t[i] ^ bplain[i])
        c2 = ''.join(map(lambda x: hex(x)[2:].rjust(2, '0'), c2))

        c3 = (x2_str + message + y2_str).encode('ascii')
        c3 = hash_func(c3)
        c3 = ''.join(map(lambda x: hex(x)[2:].rjust(2, '0'), c3))

        return SM2.hex2barray(c1 + c3 + c2)

    # klen should be aligned by 8
    @staticmethod
    def kdf(z, klen):
        assert(klen % 8 == 0)
        klen //= 8
        ret = b''
        bz = z.encode('ascii')
        ct = 0x00000001
        for i in range(klen // HASH_LENGTH + 1):
            now = bz + str(ct).rjust(8, '0').encode('ascii')
            ct += 1
            ret += hash_func(now)
        return ret[:klen]

    # cipher: byte array
    # ret value: normal ascii str
    def decrypt(self, cipher):
        c1 = cipher[:C1_LENGTH]
        c3 = cipher[C1_LENGTH: C1_LENGTH + C3_LENGTH]
        c2 = cipher[C1_LENGTH + C3_LENGTH:]

        p2 = SM2.barray2eccpoint(c1) * self.pri
        x2_str, y2_str = SM2.eccpoint2str(p2)
        klen = len(c2)
        t = SM2.kdf(x2_str + y2_str, klen * 8)

        message = bytearray()
        for i in range(len(c2)):
            message.append(t[i] ^ c2[i])
        message = message.decode('ascii')

        new_c3 = (x2_str + message + y2_str).encode('ascii')
        new_c3 = hash_func(new_c3)
        assert(new_c3 == bytearray(c3))

        return message


if __name__ == '__main__':
    x = PObject(0x4AD5F7048DE709AD51236DE65E4D4B482C836DC6E4106640)
    y = PObject(0x02BB3A02D4AAADACAE24817A4CA3A1B014B5270432DB27D2)
    g = EccPoint(x, y, ONE)
    pri = 0x58892B807074F53FBF67288A1DFAA1AC313455FE60355AFD
    a = SM2(g, pri)
    pub = g * pri
    message = 'mimaxueshiyan zhende hen you yisi'
    cipher = a.encrypt(message)
    new_plain = a.decrypt(cipher)
    print(message)
    print(cipher)
    print(new_plain)
