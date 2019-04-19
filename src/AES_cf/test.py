#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from src.AES_cf.AES import AES, get_everything_from_file
from src.AES.util import *
import src.AES_cf.cAES as caes

if __name__ == '__main__':
    key_hex_str = r'deadbeefdeadbeefdeadbeefdeadbeef'
    key_byte_list = hex_str_to_byte_list(key_hex_str)
    key_bin_list = hex_str_to_bin_list(key_hex_str, length=128)
    plain_hex_str = r'0123456789abcdeffedcba9876543210'
    plain_byte_list = hex_str_to_byte_list(plain_hex_str)
    plain_bin_list = hex_str_to_bin_list(plain_hex_str, length=128)
    cipher_hex_str = r'3b68814eb71a584c7c2a4365a9b49495'
    cipher_byte_list = hex_str_to_byte_list(cipher_hex_str)
    cipher_bin_list = hex_str_to_bin_list(cipher_hex_str, length=128)

    print('   key: {}\n plain: {}\ncipher: {}'.format(key_hex_str, plain_hex_str, cipher_hex_str))

    aes = AES(*get_everything_from_file())
    aes.tell_me_the_devil_secret(key_bin_list)
    aes_plain_hex_str = bin_list_to_hex_str(aes.decrypt(cipher_bin_list), length=32)
    aes_cipher_hex_str = bin_list_to_hex_str(aes.encrypt(plain_bin_list), length=32)
    print(' AES plain : {}\n AES cipher: {}'.format(aes_plain_hex_str, aes_cipher_hex_str))
    assert aes_cipher_hex_str == cipher_hex_str
    assert aes_plain_hex_str == plain_hex_str

    caes.tell_me_the_devil_secret(*key_byte_list)
    caes_plain_hex_str = byte_list_to_hex_str(caes.decrypt(*cipher_byte_list))
    caes_cipher_hex_str = byte_list_to_hex_str(caes.encrypt(*plain_byte_list))
    print('cAES plain : {}\ncAES cipher: {}'.format(caes_plain_hex_str, caes_cipher_hex_str))
    assert caes_cipher_hex_str == cipher_hex_str
    assert caes_plain_hex_str == plain_hex_str

    '''
    print('py begin')
    for i in range(1000):
        if i % 20 == 0:
            print(i)
        aes.encrypt(plain_bin_list)
    print('py end')
    '''

    print('c begin')
    for i in range(100000):
        caes.encrypt(*plain_byte_list)
    print('c end')
