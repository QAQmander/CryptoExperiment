#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'qaqmander'

from src.DES.util import *
from src.DES.SDES import SDES, get_everything_from_file


class DSDES(object):

    def __init__(self, *everything):
        self.sdes = SDES(*everything)
        self.__key1 = None
        self.__key2 = None

    def tell_me_the_devil_secret(self, key1, key2):
        self.__key1 = key1.copy()
        self.__key2 = key2.copy()

    def forget_the_devil_secret(self):
        self.__key1 = None
        self.__key2 = None

    def encrypt(self, plain):
        self.sdes.tell_me_the_devil_secret(self.__key1)
        temp = self.sdes.encrypt(plain)
        self.sdes.forget_the_devil_secret()
        self.sdes.tell_me_the_devil_secret(self.__key2)
        temp = self.sdes.encrypt(temp)
        self.sdes.forget_the_devil_secret()
        return temp

    def decrypt(self, cipher):
        self.sdes.tell_me_the_devil_secret(self.__key2)
        temp = self.sdes.decrypt(cipher)
        self.sdes.forget_the_devil_secret()
        self.sdes.tell_me_the_devil_secret(self.__key1)
        temp = self.sdes.decrypt(temp)
        self.sdes.forget_the_devil_secret()
        return temp


if __name__ == '__main__':
    everything = get_everything_from_file()
    dsdes = DSDES(*everything)
    test_key1 = num_to_bin_list(int('1010000010', 2), length=10)
    test_key2 = num_to_bin_list(int('0111001110', 2), length=10)
    dsdes.tell_me_the_devil_secret(test_key1, test_key2)
    plain = num_to_bin_list(int('11111101', 2), length=8)
    print(plain)
    cipher = dsdes.encrypt(plain)
    print(cipher)
    new_plain = dsdes.decrypt(cipher)
    print(new_plain)
