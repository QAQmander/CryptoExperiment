#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from random import randint
import PrimeJudge
fermat = lambda x: PrimeJudge.fermat(x, 100)

class Polynomial():    # present Polynomial

    def __init__(self, coels):
        self._coels = coels
        self._deg = len(self._coels) - 1
        if self._deg == 1 and self._coels[0] == 0:
            self._deg = -1
    
    def __str__(self):
        return self._coels[::-1].__str__()

    def __repr__(self):
        return self.__str__()

def generate(d, L, R):    # degree = d, [L, R]
    coels = [0] * (d + 1)
    t = 0
    while coels[0] == coels[1]:
        if t == 100000:    # robust
            print('Error : PrimitivePoly.generate ' \
                '-- Something wrong')
            exit(-1)
        t += 1
        coels = [0] * (d + 1)
        for i in range(d + 1):
            while True:    # generate prime in [L, R]
                b = randint(L, R)
                if fermat(b):
                    coels[i] = b
                    break
    return Polynomial(coels)

if __name__ == '__main__':
    print('degree = ')
    d = int(input())
    print('range of coefficient [L, R] : L, R = ')
    L, R = list(map(int, input().split()))
    res = generate(d, L, R)
    print(res)