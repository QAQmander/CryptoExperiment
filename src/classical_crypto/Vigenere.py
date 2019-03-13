#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from itertools import cycle

def vigenere_encode(key, plain):
    fun = lambda x, y: chr((ord(x) + ord(y) - 2 * ord('a')) % 26 + ord('a'))
    return ''.join(map(fun, cycle(key), plain))

def vigenere_decode(key, cipher):
    fun = lambda x, y: chr((ord(y) - ord(x) + 26) % 26 + ord('a'))
    return ''.join(map(fun, cycle(key), cipher))

if __name__ == '__main__':
    key = input('key ([keyword]): ')

    flag = sys.argv[1]
    if flag == '-e':
        plain = input('plain ([m]): ')
        print('cipher: ' + vigenere_encode(key, plain))
    elif flag == '-d':
        cipher = input('cipher ([c]): ')
        print('plain: ' + vigenere_decode(key, cipher))
