#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'qaqmander'

from src.DES.DES import DES, get_everything_from_file
from src.DES.util import *


class Attacker(object):

    def __init__(self, des):
        self.double_plain_and_cipher_list = None
        self.des = des
        self._l_and_r_dict_list = []
        self._length = None
        self._l_and_r_dict_list = None
        self._difference_dict_list = None

    def read_plain_and_cipher_from_file(self, filename=r'plain_and_cipher.txt'):

        def line_to_plain_and_cipher(line):
            line_after_split = line.strip().split()
            plain = hex_str_to_bin_list(line_after_split[0], length=64)
            cipher = hex_str_to_bin_list(line_after_split[1], length=64)
            return plain, cipher

        self.double_plain_and_cipher_list = []
        with open(filename, 'r') as fr:
            while True:
                first_line = fr.readline()
                if not first_line:
                    break
                second_line = fr.readline()
                self.double_plain_and_cipher_list.append(
                    (
                        line_to_plain_and_cipher(first_line),
                        line_to_plain_and_cipher(second_line)
                    )
                )
        # print(self.double_plain_and_cipher_list)

    def attack(self):
        self._length = len(self.double_plain_and_cipher_list[0][0][0])
        self._calculate_l_and_r()
        self._calculate_difference()

    def _calculate_l_and_r(self):
        self._l_and_r_dict_list = []
        for index in range(len(self.double_plain_and_cipher_list)):
            double_plain_and_cipher = self.double_plain_and_cipher_list[index]
            self._l_and_r_dict_list.append({})
            for i in range(2):
                plain_after_ip = self.des.ip(double_plain_and_cipher[i][0])
                plain_l, plain_r = plain_after_ip[:self._length // 2], plain_after_ip[self._length // 2:]
                cipher_before_ip_inv = self.des.ip(double_plain_and_cipher[i][1])
                cipher_l, cipher_r = cipher_before_ip_inv[self._length // 2:], cipher_before_ip_inv[:self._length // 2]
                if i == 0:
                    self._l_and_r_dict_list[index]['normal'] = {
                        'plain': {'l': plain_l, 'r': plain_r},
                        'cipher': {'l': cipher_l, 'r': cipher_r}
                    }
                else:
                    self._l_and_r_dict_list[index]['star'] = {
                        'plain': {'l': plain_l, 'r': plain_r},
                        'cipher': {'l': cipher_l, 'r': cipher_r}
                    }
        # for l_and_r_dict in self._l_and_r_dict_list:
        #     print(bin_list_to_hex_str(l_and_r_dict['normal']['plain']['l'], length=16),
        #         l_and_r_dict['normal']['cipher'])
        #     print(bin_list_to_hex_str(l_and_r_dict['star']['plain']['l'], length=16),
        #         l_and_r_dict['star']['cipher'])

    def _calculate_difference(self):
        self._difference_dict_list = []
        for index in range(len(self._l_and_r_dict_list)):
            l_and_r_dict = self._l_and_r_dict_list[index]
            self._difference_dict_list.append({})
            self._difference_dict_list[index]['e_normal'] = des.e(l_and_r_dict['normal']['cipher']['l'])
            self._difference_dict_list[index]['e_star'] = des.e(l_and_r_dict['star']['cipher']['l'])
            self._difference_dict_list[index]['output'] = \
                get_map_from_order_number_table(get_inv_from_order_number_list(des.source['p']))(
                    xor(
                        xor(
                            l_and_r_dict['normal']['plain']['l'],
                            l_and_r_dict['star']['plain']['l']
                        ),
                        xor(
                            l_and_r_dict['normal']['cipher']['r'],
                            l_and_r_dict['star']['cipher']['r']
                        )
                    )
                )
        # print(''.join(map(str, self._difference_dict_list[0]['e_normal'])))
        # print(''.join(map(str, self._difference_dict_list[0]['e_star'])))
        # print(''.join(map(str, self._difference_dict_list[0]['output'])))


if __name__ == '__main__':
    everything = get_everything_from_file()
    des = DES(*everything)
    # test_key_hex_str = r'133457799BBCDFF1'
    # r_hex_str = r'12345678'
    # l_hex_str_list = [r'12345678', r'3456789a']  # , r'abcdef99']
    # xor_res = r'deadbeef'
    # des.tell_me_the_devil_secret(hex_str_to_bin_list(test_key_hex_str, length=64))
    # with open(r'plain_and_cipher.txt', 'w') as fw:
    #     for i in range(len(l_hex_str_list)):
    #         l_hex_str = l_hex_str_list[i]
    #         plain = des.ip_inv(hex_str_to_bin_list(l_hex_str + r_hex_str, length=64))
    #         cipher = des.encrypt(plain, turn=3)
    #         fw.write(bin_list_to_hex_str(plain, length=16) + ' ' + bin_list_to_hex_str(cipher, length=16) + '\n')
    #         plain_star = xor(plain, hex_str_to_bin_list(xor_res, length=64))
    #         cipher_star = des.encrypt(plain_star, turn=3)
    #         fw.write(
    #             bin_list_to_hex_str(plain_star, length=16) + ' ' + bin_list_to_hex_str(cipher_star, length=16) + '\n')
    # des.forget_the_devil_secret()
    plain = bin_list_to_hex_str(des.ip_inv(hex_str_to_bin_list('748502CD38451097', length=64)), length=16)
    cipher = bin_list_to_hex_str(des.ip_inv(swap(hex_str_to_bin_list('03C70306D8A09F10', length=64))), length=16)
    plain_star = bin_list_to_hex_str(des.ip_inv(hex_str_to_bin_list('3874756438451097', length=64)), length=16)
    cipher_star = bin_list_to_hex_str(des.ip_inv(swap(hex_str_to_bin_list('78560A0960E6D4CB', length=64))), length=16)
    with open(r'plain_and_cipher.txt', 'w') as fw:
        fw.write(plain + ' ' + cipher + '\n')
        fw.write(plain_star + ' ' + cipher_star + '\n')
    attacker = Attacker(des)
    attacker.read_plain_and_cipher_from_file()
    attacker.attack()

