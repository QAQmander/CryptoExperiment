#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'qaqmander'

from src.DES.util import *
from src.infrastructure.util import *


class SDES(object):

    def __init__(self, ip, ip_inv, e, s, p, p10, p8):
        self.src = {
            'ip': ip.copy(),
            'ip_inv': ip_inv.copy(),
            'e': e.copy(),
            's': [s[0].copy(), s[1].copy()],
            'p': p.copy(),
            'p10': p10.copy(),
            'p8': p8.copy()
        }
        self.ip = get_map_from_order_number_table(ip)
        self.ip_inv = get_map_from_order_number_table(ip_inv)
        self.e = get_map_from_order_number_table(e)
        self.s = []
        for i in range(2):
            self.s.append(
                (lambda i:
                 lambda bin_list:
                 self.src['s'][i][
                     4 * bin_list_to_num([bin_list[0], bin_list[3]])
                     + bin_list_to_num([bin_list[1], bin_list[2]])
                     ])(i)
            )
        self.p = get_map_from_order_number_table(p)
        self.p10 = get_map_from_order_number_table(p10)
        self.p8 = get_map_from_order_number_table(p8)
        self.__key = None

    def tell_me_the_devil_secret(self, key):
        self.__key = key.copy()

    def forget_the_devil_secret(self):
        self.__key = None

    def encrypt(self, plain, turn=2):
        encrypt_subkey_list = self.calculate_subkey_list()
        return self._do_something(plain, encrypt_subkey_list, turn)

    def decrypt(self, cipher, turn=2):
        decrypt_subkey_list = self.calculate_subkey_list()
        return self._do_something(cipher, decrypt_subkey_list.reverse() or decrypt_subkey_list, turn)

    def calculate_subkey_list(self):
        after_p10 = self.p10(self.__key)
        left, right = after_p10[:5], after_p10[5:]
        subkey_list = []
        for i in range(2):
            left = left[i + 1:] + left[:i + 1]
            right = right[i + 1:] + right[:i + 1]
            subkey_list.append(self.p8(left + right))
        return subkey_list

    def _feistel(self, plain, subkey):
        after_e = self.e(plain)
        after_xor = xor(after_e, subkey)
        left, right = after_xor[:4], after_xor[4:]
        # print(left, right)
        left = num_to_bin_list(self.s[0](left), length=2)
        right = num_to_bin_list(self.s[1](right), length=2)
        # print(left, right)
        after_s = left + right
        after_p = self.p(after_s)
        return after_p

    def _do_something(self, plain, subkey_list, turn):
        after_ip = self.ip(plain)
        left, right = after_ip[:4], after_ip[4:]
        for i in range(turn):
            next_left = right
            next_right = xor(left, self._feistel(right, subkey_list[i]))
            left, right = next_left, next_right
        left, right = right, left
        return self.ip_inv(left + right)


def get_everything_from_file(filename=r'SDES.txt'):
    def get_two_lines_to_list(f, offset=0):
        return f.readline() and list(map(lambda x: int(x) + offset, f.readline().strip().split()))

    with open(filename, 'r') as fr:
        ret_ip = get_two_lines_to_list(fr, -1)
        ret_ip_inv = get_two_lines_to_list(fr, -1)
        ret_e = get_two_lines_to_list(fr, -1)
        ret_s = []
        for i in range(2):
            ret_s.append(get_two_lines_to_list(fr))
        # print(ret_s)
        ret_p = get_two_lines_to_list(fr, -1)
        ret_p10 = get_two_lines_to_list(fr, -1)
        ret_p8 = get_two_lines_to_list(fr, -1)
    return ret_ip, ret_ip_inv, ret_e, ret_s, ret_p, ret_p10, ret_p8


if __name__ == '__main__':
    everything = get_everything_from_file()
    sdes = SDES(*everything)
    test_key1 = num_to_bin_list(int('1010000010', 2), length=10)
    test_key2 = num_to_bin_list(int('0101010101', 2), length=10)
    sdes.tell_me_the_devil_secret(test_key1)
    plain = hex_str_to_bin_list('dd', length=8)
    print(plain)
    cipher = sdes.encrypt(plain)
    print(cipher)
    new_plain = sdes.decrypt(cipher)
    print(new_plain)

