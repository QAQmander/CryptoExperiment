#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from itertools import cycle


def vernam_encode(key, plain):
    fun = lambda x, y: '0' if x == y else '1'
    return ''.join(map(fun, cycle(key), plain))


vernam_decode = vernam_encode

if __name__ == '__main__':
    key = input('key ([keyword]): ')

    flag = sys.argv[1]
    if flag == '-e':
        plain = input('plain ([m]): ')
        print('cipher: ' + vernam_encode(key, plain))
    elif flag == '-d':
        cipher = input('cipher ([c]): ')
        print('plain: ' + vernam_decode(key, cipher))
