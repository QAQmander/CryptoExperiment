#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from random import randint
import PrimeJudge
fermat = lambda x: PrimeJudge.fermat(x, 100)

class Polynomial():

    def __init__(self, coels):
        self._coels = coels
        self._deg = len(self._coels) - 1
        if self._deg == 1 and self._coels[0] == 0:
            self._deg = -1
    
    def __str__(self):
        return self._coels[::-1].__str__()

    def __repr__(self):
        return self.__str__()

def generate(d, L, R):
    coels = [0] * (d + 1)
    for i in range(d + 1):
        while True:
            b = randint(L, R)
            if fermat(b) and not b in coels:
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