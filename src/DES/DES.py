#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'qaqmander'

from itertools import cycle


def _bin_list_to_hex_str(bin_list):
    return hex(_bin_list_to_num(bin_list))[2:]


def _hex_str_to_bin_list(hex_string, length):
    return _num_to_bin_list(int(hex_string, 16), length)


def _bin_list_to_num(bin_list):
    return int(''.join(map(str, bin_list)), 2)


def _num_to_bin_list(num, length):
    return list(map(int, bin(num)[2:].rjust(length, '0')))


class DES(object):
    def __init__(self, ip, ip_inv, e, p, s, pc1, pc2, flag, length=64, s_box_output_length=4):
        self._ip = lambda xs: [xs[index] for index in ip]
        if not ip_inv:
            ip_inv = [ip.find(index) for index in range(length)]
        self._ip_inv = lambda bin_list: [bin_list[index] for index in ip]
        self._e = lambda bin_list: [bin_list[index] for index in e]
        self._p = lambda bin_list: [bin_list[index] for index in p]
        self._s = [(lambda si:
                    (lambda bin_list:
                     ((lambda table_number, bin_list_middle: _num_to_bin_list(
                         si[table_number * 2 ** s_box_output_length + _bin_list_to_num(bin_list_middle)],
                         length=s_box_output_length))
                      (_bin_list_to_num([bin_list[0], bin_list[-1]]), bin_list[1:-1]))))(si.copy())
                   for si in s]
        # print((self._s[0]([1, 1, 1, 1, 1, 1])))
        self._pc1 = lambda bin_list: [bin_list[index] for index in pc1]
        self._pc2 = lambda bin_list: [bin_list[index] for index in pc2]
        self._flag = lambda turn_number: flag[turn_number]  # unnecessary but interesting
        self.___key = None  # SECRET!!!

    def tell_me_secret(self, key):
        self.___key = key

    def _calculate_subkey_list(self, turn=16):
        print(self.___key)
        after_pc1 = self._pc1(self.___key)
        length = len(after_pc1)
        now_subkey_0, now_subkey_1 = after_pc1[:length // 2].copy(), after_pc1[length // 2:].copy()
        subkey_list = []
        for turn_number in range(turn):
            # print(self._flag(turn_number))
            # print(len(nowkey_0), len(nowkey_1))
            # print(now_subkey_0)
            now_subkey_0, now_subkey_1 = map(lambda key:
                                     ((lambda cycle_key:
                                       [next(cycle_key) for bit_number in
                                        range(length // 2 + self._flag(turn_number))][self._flag(turn_number):])
                                      (cycle(key))),
                                     (now_subkey_0, now_subkey_1))
            # print(now_subkey_0)
            # print(len(nowkey_0), len(nowkey_1))
            subkey_list.append(self._pc2(now_subkey_0.copy() + now_subkey_1.copy()))
        return subkey_list


def get_everything_from_file(filename='DES.txt'):
    def get_two_lines_to_list(f, offset=0):
        return f.readline() and list(map(lambda x: int(x) + offset, f.readline().strip().split(',')))

    with open(filename, 'r') as fr:
        ret_ip = get_two_lines_to_list(fr, -1)
        ret_ip_inv = get_two_lines_to_list(fr, -1)
        ret_e = get_two_lines_to_list(fr, -1)
        ret_p = get_two_lines_to_list(fr, -1)
        ret_s = []
        for i in range(8):
            ret_s.append(get_two_lines_to_list(fr))
        ret_pc1 = get_two_lines_to_list(fr, -1)
        ret_pc2 = get_two_lines_to_list(fr, -1)
        ret_flag = get_two_lines_to_list(fr)
    return ret_ip, ret_ip_inv, ret_e, ret_p, ret_s, ret_pc1, ret_pc2, ret_flag


if __name__ == '__main__':
    # print(_bin_list_to_num([1, 0, 1]))
    # print(_num_to_bin_list(64, length=32))
    # print(_bin_list_to_hex_str([1, 1, 1, 1, 0, 0, 1, 1]))
    # print(_hex_str_to_bin_list('ffffaaaa', length=32))
    everything = get_everything_from_file()
    des = DES(*everything)
    test_key = _hex_str_to_bin_list('133457799bbcdff1', length=64)
    des.tell_me_secret(test_key)
    # subkey_list = des._calculate_subkey_list()
    # for subkey in subkey_list:
    #     print(''.join(map(str, subkey)))

