#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'qaqmander'

import pickle

from src.DES.DES import DES
from src.DES.util import *


class Attacker(object):

    def __init__(self, des, filename=None):
        self.double_plain_and_cipher_list = None
        self.des = des
        self._l_and_r_dict_list = []
        self._length = None
        self._l_and_r_dict_list = None
        self._difference_dict_list = None
        self._possible_key3_list = None
        self.qaqmander = None    # result
        self._s_box_difference_dict_list = []
        if not filename:
            for index in range(8):
                self._s_box_difference_dict_list.append({})
                for input_difference_num in range(1 << 6):
                    self._s_box_difference_dict_list[index][input_difference_num] = {}
                    for input_num in range(1 << 6):
                        output_difference_num = bin_list_to_num(xor(
                            self.des.temp_s[index](num_to_bin_list(input_num, length=6)),
                            self.des.temp_s[index](num_to_bin_list(input_num ^ input_difference_num, length=6))
                        ))
                        if not self._s_box_difference_dict_list[index][input_difference_num].get(output_difference_num,
                                                                                                 None):
                            self._s_box_difference_dict_list[index][input_difference_num][output_difference_num] = set()
                        self._s_box_difference_dict_list[index][input_difference_num][output_difference_num].add(
                            input_num)
            with open(r's_box_difference_dict_list', 'wb') as fw:
                pickle.dump(self._s_box_difference_dict_list, fw)
        else:
            with open(filename, 'rb') as fr:
                self._s_box_difference_dict_list = pickle.load(fr)

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
        self._calculate_possible_key3_set()
        # print(self._possible_key3_list)
        key3_48 = []
        for i in range(8):
            key3_48.extend(num_to_bin_list(list(self._possible_key3_list[i])[0], length=6))
        key_56_before_pc2 = [-1] * 56
        pc2_list = self.des.source['pc2']
        for i in range(48):
            key_56_before_pc2[pc2_list[i]] = key3_48[i]
        key_56 = []
        key_56 += key_56_before_pc2[24:28]
        key_56 += key_56_before_pc2[0:24]
        key_56 += key_56_before_pc2[52:56]
        key_56 += key_56_before_pc2[28:52]
        test_plain = self.double_plain_and_cipher_list[0][0][0]
        test_cipher = self.double_plain_and_cipher_list[0][0][1]
        for i in range(1 << 8):
            attempt_patch = num_to_bin_list(i, length=8)
            attempt_key_56 = key_56.copy()
            k = 0
            for j in range(56):
                if attempt_key_56[j] == -1:
                    attempt_key_56[j] = attempt_patch[k]
                    k += 1
            attempt_key_64 = [-1] * 64
            pc1_list = self.des.source['pc1']
            # print(pc1_list)
            for j in range(56):
                attempt_key_64[pc1_list[j]] = attempt_key_56[j]
            for j in range(8):
                xor_res = 0
                for k in range(7):
                    xor_res ^= attempt_key_64[8 * j + k]
                attempt_key_64[8 * j + 7] = 1 - xor_res
            self.des.tell_me_the_devil_secret(attempt_key_64)
            if self.des.encrypt(test_plain, turn=3) == test_cipher:
                self.qaqmander = attempt_key_64
                self.des.forget_the_devil_secret()
                break
            self.des.forget_the_devil_secret()
        # print(bin_list_to_hex_str(self.qaqmander, length=16))
        return self.qaqmander

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

    def _calculate_possible_key3_set(self):
        self._possible_key3_list = [set(range(1 << 6)) for i in range(8)]
        for index in range(len(self._difference_dict_list)):
            difference_dict = self._difference_dict_list[index]
            e_normal_list = [bin_list_to_num(difference_dict['e_normal'][6 * i: 6 * (i + 1)]) for i in range(8)]
            input_difference = xor(difference_dict['e_normal'], difference_dict['e_star'])
            input_difference_num_list = [bin_list_to_num(input_difference[6 * i: 6 * (i + 1)]) for i in range(8)]
            output_difference = difference_dict['output']
            output_difference_num_list = [bin_list_to_num(output_difference[4 * i: 4 * (i + 1)]) for i in range(8)]
            for j in range(8):
                possible_key3 = set(map(
                    lambda possible_input_num: possible_input_num ^ e_normal_list[j],
                    self._s_box_difference_dict_list[j][input_difference_num_list[j]].get(output_difference_num_list[j],
                                                                                          set())
                ))
                self._possible_key3_list[j] = self._possible_key3_list[j].intersection(possible_key3)
        # print(self._possible_key3_list)


def from_pdf_to_plain_and_cipher(des, input_filename=r'plain_and_cipher_from_pdf.txt', output_filename=r'plain_and'
                                                                                                       r'_cipher.txt'):
    with open(input_filename, 'r') as fr:
        with open(output_filename, 'w') as fw:
            while True:
                first_line = fr.readline()
                if not first_line:
                    break
                first_line = first_line.strip().split()
                second_line = fr.readline().strip().split()
                plain = bin_list_to_hex_str(des.ip_inv(hex_str_to_bin_list(first_line[0], length=64)), length=16)
                cipher = bin_list_to_hex_str(des.ip_inv(swap(hex_str_to_bin_list(first_line[1], length=64))), length=16)
                plain_star = bin_list_to_hex_str(des.ip_inv(hex_str_to_bin_list(second_line[0], length=64)), length=16)
                cipher_star = bin_list_to_hex_str(des.ip_inv(swap(hex_str_to_bin_list(second_line[1], length=64))),
                                                  length=16)
                fw.write(plain + ' ' + cipher + '\n')
                fw.write(plain_star + ' ' + cipher_star + '\n')


if __name__ == '__main__':
    everything = get_everything_from_file()
    des = DES(*everything)
    test_key_hex_str = make_it_look_like_a_real_key_hex_str(r'fafafafa12345678')
    print('test_key_hex_str  : ' + test_key_hex_str)
    # print(hex_str_to_bin_list(test_key_hex_str, length=64))
    # print(des.pc1(hex_str_to_bin_list(test_key_hex_str, length=64)))
    l_hex_str_list = [r'12345678', r'3456789a', r'12345678', r'3456789a', r'87654321', r'bcbc1245']
    r_hex_str_list = [r'deadbeef', r'cafebabe', r'abcd1234']
    des.tell_me_the_devil_secret(hex_str_to_bin_list(test_key_hex_str, length=64))

    with open(r'plain_and_cipher.txt', 'w') as fw:
        for i in range(len(r_hex_str_list)):
            l_hex_str = l_hex_str_list[2 * i]
            r_hex_str = r_hex_str_list[i]
            plain = des.ip_inv(hex_str_to_bin_list(l_hex_str + r_hex_str, length=64))
            cipher = des.encrypt(plain, turn=3)
            fw.write(bin_list_to_hex_str(plain, length=16) + ' ' + bin_list_to_hex_str(cipher, length=16) + '\n')
            l_hex_str = l_hex_str_list[2 * i + 1]
            r_hex_str = r_hex_str_list[i]
            plain = des.ip_inv(hex_str_to_bin_list(l_hex_str + r_hex_str, length=64))
            cipher = des.encrypt(plain, turn=3)
            fw.write(bin_list_to_hex_str(plain, length=16) + ' ' + bin_list_to_hex_str(cipher, length=16) + '\n')
    des.forget_the_devil_secret()
    # from_pdf_to_plain_and_cipher(des)
    attacker = Attacker(des, filename=r's_box_difference_dict_list')
    attacker.read_plain_and_cipher_from_file()
    attacker.attack()
    print('attacker.qaqmander: ' + bin_list_to_hex_str(attacker.qaqmander, length=16))
    assert test_key_hex_str == bin_list_to_hex_str(attacker.qaqmander, length=16)
