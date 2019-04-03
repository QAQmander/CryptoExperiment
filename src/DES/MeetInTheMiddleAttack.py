#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'qaqmander'

from src.infrastructure.util import *
from src.DES.DoubleSDES import DoubleSDES
from src.DES.SDES import SDES, get_everything_from_file


class Attacker(object):

    def __init__(self, *everything):
        self.sdes = SDES(*everything)
        self.dsdes = DoubleSDES(*everything)
        self.test_plain, self.test_cipher = None, None
        self.check = []
        self._dict = {}

    def read_plain_and_cipher_from_file(self, filename=r'meet_in_the_middle.txt'):
        with open(filename, 'r') as fr:
            line = fr.readline().strip().split()
            self.test_plain = hex_str_to_bin_list(line[0], length=8)
            self.test_cipher = hex_str_to_bin_list(line[1], length=8)
            line = fr.readline()
            while line:
                line = line.strip().split()
                self.check.append({
                    'plain': hex_str_to_bin_list(line[0], length=8),
                    'cipher': hex_str_to_bin_list(line[1], length=8)
                })
                line = fr.readline()
        # print(self.test_plain)
        # print(self.test_cipher)
        # print(self.check_plain)
        # print(self.check_cipher)

    def attack(self):
        for test_key_num in range(1 << 10):
            test_key = num_to_bin_list(test_key_num, length=10)
            self.sdes.tell_me_the_devil_secret(test_key)
            self._dict[test_key_num] = self.sdes.encrypt(self.test_plain)
            self.sdes.forget_the_devil_secret()
        # print(bin_list_to_hex_str(self._dict[642], length=2))
        ret = []
        for test_key_num in range(1 << 10):
            test_key = num_to_bin_list(test_key_num, length=10)
            self.sdes.tell_me_the_devil_secret(test_key)
            temp = self.sdes.decrypt(self.test_cipher)
            for key_num in self._dict.keys():
                if temp == self._dict[key_num]:
                    self.dsdes.tell_me_the_devil_secret(num_to_bin_list(key_num, length=10), test_key)
                    flag = True
                    for plain_and_cipher in self.check:
                        res = self.dsdes.encrypt(plain_and_cipher['plain'])
                        if res != plain_and_cipher['cipher']:
                            flag = False
                            break
                    if flag:
                        ret.append((num_to_bin_list(key_num, length=10), test_key.copy()))
        return ret


if __name__ == '__main__':
    everything = get_everything_from_file()
    attacker = Attacker(*everything)
    attacker.read_plain_and_cipher_from_file()
    ret = attacker.attack()
    for item in ret:
        print(item)
    # key1, key2 = attacker.attack()
    # print(key1)
    # print(key2)


