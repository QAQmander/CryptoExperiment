#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from random import randint
from src.infrastructure.Euclid import gcd_const
from src.infrastructure.Power import pow_fast_m


def fermat(n, t):  # judge n, for t times
    if n <= 1:
        return False
    while t:  # for t times
        b = randint(1, n - 1)  # b <- random num
        d = gcd_const(n, b)[2]  # get gcd of n & b
        if d != 1:
            return False
        b = pow_fast_m(b, n - 1, n)  # compute b ^ (n - 1) mod n
        if d != 1:
            return False
        t -= 1
    return True


def _v2(n):  # get k, q for n - 1 = q * 2 ^ k where q is odd
    k, q = 0, n
    while not (q & 1):
        k, q = k + 1, q // 2
    return k, q


def miller_rabin(n, t):  # judge n, for t times
    if n <= 1:
        return False
    k, q = _v2(n - 1)  # get k, q
    while t:  # for t times
        a = randint(2, n - 2)  # a <- random num
        a = pow_fast_m(a, q, n)
        flag = False
        if a == 1:  # whether a ^ q == 1 ( mod n )
            flag = True
        for j in range(k):  # whether a ^ {2 ^ j * q} == 1 ( mod n )
            if a == n - 1:
                flag = True
                break
            a = a ** 2 % n
        if not flag:
            return False
        t -= 1
    return True


def _jacobi(a, b, coe):  # compute jacobi symbol
    d = gcd_const(a, b)[2]
    if d > 1:
        return 0
    k, q = _v2(a)
    ncoe = coe
    ncoe *= (-1) ** ((q - 1) * (b - 1) // 4)
    if k & 1:
        ncoe *= (-1) ** ((b ** 2 - 1) // 8)
    if q == 1:
        return ncoe
    return _jacobi(b % q, q, ncoe)


def solovay_stassen(n, t):  # judge n, for t times
    if n <= 1:
        return False
    if not n & 1:  # judge whether n is even
        return False
    while t:
        b = randint(2, n - 2)
        r = pow_fast_m(b, (n - 1) // 2, n)
        if r == n - 1:
            r = -1
        if r != 1 and r != -1:
            return False
        s = _jacobi(b, n, 1)  # compute jacobi symbol
        if r != s:
            # print(b, n, r, s)
            return False
        t -= 1
    return True


if __name__ == '__main__':
    # t = int(sys.argv[1])
    # n = int(input())
    t = 10
    n = 2 ** 127 - 1
    if solovay_stassen(n, t):
        print('Congratulation! {} is prime!'.format(n))
    else:
        print('What a pity! {} is not prime!'.format(n))
