#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def pow_normal(x, n):  # normal algorithm [O(n)]
    # int, int -> int
    ret = 1
    for i in range(n):
        ret *= x
    return ret


def pow_fast(x, n):  # fast algorithm according to binary representation
    # [O(log(n))]
    # int, int -> int
    res = 1
    while n:
        if n % 2 == 0:  # if n is even ...
            x, n, res = x ** 2, n // 2, res
        else:  # if n is odd ...
            x, n, res = x, n - 1, res * x
    return res


def pow_fast_m(x, n, m):
    res = 1
    while n:
        if n % 2 == 0:
            x, n, res = x ** 2 % m, n // 2, res
        else:
            x, n, res = x, n - 1, res * x % m
    return res


if __name__ == '__main__':
    x, n = list(map(int, input().split()))
    if not x:  # for robustness
        print('You will always get ZERO because x is ZERO.')
    if n < 0:  # for robustness
        print('n should be positive!')
    res = pow_fast(x, n)
    print(res)
