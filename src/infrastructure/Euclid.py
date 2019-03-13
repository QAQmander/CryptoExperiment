#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class GcdRes(object):
    def __init__(self, x, y, d):
        self.x = x
        self.y = y
        self.d = d

    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        elif index == 2:
            return self.d
        else:
            raise KeyError


def gcd_increment(a, b):  # recursive, all saved
    # int, int -> int, int, int
    # a, b -> x, y, d : so that ax + by = d
    if not b:
        return 1, 0, a
    else:
        x1, y1, d = gcd_increment(b, a % b)  # recursive
        k = a // b
        return y1, x1 - k * y1, d  # calc x, y from x1, y1
        # x = y1; y = x1 - k * y1
        #     where k = a div b


def gcd_const(a, b):  # only last two steps saved
    # int, int -> int, int, int
    # a, b -> x, y, d : so that ax + by = d
    xa, ya, xb, yb = 1, 0, 0, 1  # initial
    while b:
        k = a // b
        xa, ya, xb, yb = xb, yb, xa - k * xb, ya - k * yb
        #   always keep now_a = xa * ini_a + ya * ini_b
        #               now_b = xb * ini_a + yb * ini_b
        a, b = b, a % b
    return xa, ya, a


def gcd(a, b):
    x, y, d = gcd_const(a, b)
    return GcdRes(x, y, d)


def inv(a, b):
    res = gcd(a, b)
    if res.d != 1:
        print('Error : Euclid.inv -- %d and '
              '%d are not coprime' % (a, b))
        exit(-1)
    return res.x


if __name__ == '__main__':
    a, b = list(map(int, input().split()))
    if not a and not b:  # for robustness
        print('Something wrong...')
    else:
        s, t, d = gcd_const(a, b)
        print(s, t, d)
