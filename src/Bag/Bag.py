#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from random import randint
from src.infrastructure.Euclid import gcd_const


class Bag(object):

    def __init__(self):
        self.prime = 100000007
        self.pri = None
        self.pub = None
        self.len = None
        self.w = None
        self.w_inv = None

    def key_gen(self):
        self.pri = [1]
        sum = 1
        while sum < self.prime:
            now = randint(sum + 1, 2 * sum)
            sum += now
            self.pri.append(now)
        self.pri.pop()
        self.len = len(self.pri)
        while True:
            w = randint(2, self.prime - 1)
            self.pub = list(map(lambda x: x * w % self.prime, self.pri))
            now = sorted(self.pub)
            sum = 0
            flag = False
            for i in now:
                if sum > i:
                    flag = True
                    break
                sum += i
            if flag:
                self.w = w
                self.w_inv = gcd_const(w, self.prime)[0]
                break

    def encode(self, plain):
        ret = 0
        for i in range(self.len):
            ret += (self.pub[i] * plain[i]) % self.prime
        return ret

    def decode(self, cipher):
        ret = []
        cipher = cipher * self.w_inv % self.prime
        for i in range(len(self.pri) - 1, -1, -1):
            now = 1 if cipher >= self.pri[i] else 0
            cipher -= now * self.pri[i]
            ret.append(now)
        ret.reverse()
        return ret


class Attacker(object):

    def __init__(self, pub, prime):
        self.pub = pub
        self.prime = prime
        self.pri = None
        self.w = None
        self.w_inv = None

    def attack(self):
        while True:
            w_inv = randint(2, self.prime - 1)
            # w_inv = b.w_inv
            self.pri = list(map(lambda x: x * w_inv % self.prime, self.pub))
            now = sorted(self.pri)
            sum = 0
            flag = True
            for i in now:
                if sum >= i:
                    flag = False
                sum += i
            if flag:
                self.w_inv = w_inv
                self.w = gcd_const(w_inv, self.prime)[0]
                break

    def decode(self, cipher):
        ret = []
        cipher = cipher * self.w_inv % self.prime
        for i in range(len(self.pri) - 1, -1, -1):
            now = 1 if cipher >= self.pri[i] else 0
            cipher -= now * self.pri[i]
            ret.append(now)
        ret.reverse()
        return ret

if __name__ == '__main__':
    b = Bag()
    b.key_gen()
    plain = [1, 0] * (b.len // 2)
    if b.len % 2 != 0:
        plain.append(1)
    cipher = b.encode(plain)
    new_plain = b.decode(cipher)
    print('private:', b.pri)
    print('public:', b.pub)
    print('prime:', b.prime)
    print('plain:', plain)
    print('cipher:', cipher)
    print('new_plain:', new_plain)
    a = Attacker(b.pub, b.prime)

    a.attack()
    attres = a.decode(cipher)
    assert attres == plain

