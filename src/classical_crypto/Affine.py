#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from src.infrastructure.Euclid import gcd


def affine_encode(key, plain):
    a, b = key
    cipher = ''
    for char in plain:
        cipher += chr(((ord(char) - ord('a')) * a + b) % 26 + ord('a'))
    return cipher


def affine_decode(key, cipher):
    ai, b = gcd(key[0], 26).x, key[1]
    plain = ''
    for char in cipher:
        plain += chr(((ord(char) - ord('a') - b + 26) * ai) % 26 + ord('a'))
    return plain


if __name__ == '__main__':
    key = list(map(int, input('key ([a] [b]): ').split()))
    if gcd(key[0], 26).d != 1:
        print('Error : a should be coprime with 26')
        exit(-1)

    flag = sys.argv[1]
    if flag == '-e':
        plain = input('plain ([m]): ')
        print('cipher: ' + affine_encode(key, plain))
    elif flag == '-d':
        cipher = input('cipher ([c]): ')
        print('plain: ' + affine_decode(key, cipher))
