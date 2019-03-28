#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'qaqmander'

from src.DES.DES import DES
from src.DES.util import *


class TripleDES(object):

    def __init__(self, *everything):
        self._des1 = DES(*everything)
        self._des2 = DES(*everything)

    def tell_me_the_devil_secret(self, key):
        self._des1.tell_me_the_devil_secret(key[:64].copy())
        self._des2.tell_me_the_devil_secret(key[64:].copy())

    def forget_the_devil_secret(self):
        self._des2.forget_the_devil_secret()
        self._des1.forget_the_devil_secret()

    def encrypt(self, plain, turn=16):
        return self._des1.encrypt(self._des2.decrypt(self._des1.encrypt(plain, turn), turn), turn)

    def decrypt(self, cipher, turn=16):
        return self._des1.decrypt(self._des2.encrypt(self._des1.decrypt(cipher, turn), turn), turn)


if __name__ == '__main__':
    everything = get_everything_from_file()
    tdes = TripleDES(*everything)
    test_key_hex_str = make_it_look_like_a_real_key_hex_str(r'cafebabedeadbeefdeadbeefcafebabe')
    test_key = hex_str_to_bin_list(test_key_hex_str, length=128)
    tdes.tell_me_the_devil_secret(test_key)

    plain_hex_str = r'0123456789abcdef'
    plain = hex_str_to_bin_list(plain_hex_str, length=64)
    print('plain_hex_str: ' + plain_hex_str)

    cipher = tdes.encrypt(plain)
    cipher_hex_str = bin_list_to_hex_str(cipher, length=16)
    print('cipher_hex_str: ' + cipher_hex_str)

    plain_again = tdes.decrypt(cipher)
    plain_again_hex_str = bin_list_to_hex_str(plain, length=16)
    print('plain_again: ' + plain_again_hex_str)
