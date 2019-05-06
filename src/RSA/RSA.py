#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from random import randint
from src.infrastructure.PrimeJudge import miller_rabin
prime_judge = lambda x: miller_rabin(x, 500)
from src.infrastructure.Euclid import gcd_const
from src.infrastructure.CRT import CRT


class RSA(object):

    def __init__(self):
        self.n = None
        self.e = None
        self.d = None
        self.p = None
        self.q = None
        self.fai = None

    @staticmethod
    def prime_gen(length=512):
        p = randint(2**length, 2**(length+1))
        if p % 2 == 0:
            p += 1
        while True:
            if prime_judge(p):
                return p
            else:
                p += 2

    @staticmethod
    def key_gen(filename=r'rsa'):
        pub_filename = filename + '_pub'
        pri_filename = filename + '_pri'
        p = RSA.prime_gen()
        q = RSA.prime_gen()
        n = p * q
        fai = (p - 1) * (q - 1)
        print(pow(3, fai, n))
        while True:
            e = randint(103, p - 1)
            if gcd_const(e, fai)[2] == 1:
                break
        d = gcd_const(e, fai)[0] % fai
        with open(pub_filename, 'w') as fw:
            fw.write('{}\n'.format(hex(n)[2:]))
            fw.write('{}\n'.format(hex(e)[2:]))
        with open(pri_filename, 'w') as fw:
            fw.write('{}\n'.format(hex(p)[2:]))
            fw.write('{}\n'.format(hex(q)[2:]))
            fw.write('{}\n'.format(hex(d)[2:]))

    def tell_me_the_holy_secret(self, filename=r'rsa'):
        pub_filename = filename + '_pub'
        with open(pub_filename, 'r') as fr:
            self.n = int(fr.readline().strip(), 16)
            self.e = int(fr.readline().strip(), 16)

    def forget_the_holy_secret(self):
        self.n = None
        self.e = None

    def encode_single(self, plain):
        return pow(plain, self.e, self.n)

    def tell_me_the_devil_secret(self, filename=r'rsa'):
        pri_filename = filename + '_pri'
        with open(pri_filename, 'r') as fr:
            self.p = int(fr.readline().strip(), 16)
            self.q = int(fr.readline().strip(), 16)
            self.d = int(fr.readline().strip(), 16)
        self.fai = (self.p - 1) * (self.q - 1)

    def forget_the_devil_secret(self):
        self.p = None
        self.q = None
        self.d = None

    def decode_single(self, cipher):
        res_p, res_q = pow(cipher, self.d, self.p), pow(cipher, self.d, self.q)
        return CRT((self.p, self.q), (res_p, res_q))[0]


if __name__ == '__main__':
    # RSA.key_gen()
    rsa = RSA()
    rsa.tell_me_the_holy_secret()
    cipher = rsa.encode_single(12389031280932)
    rsa.forget_the_holy_secret()
    print('cipher: ', hex(cipher))
    rsa.tell_me_the_devil_secret()
    new_plain = rsa.decode_single(cipher)
    rsa.forget_the_devil_secret()
    print('new_plain: ', new_plain)

