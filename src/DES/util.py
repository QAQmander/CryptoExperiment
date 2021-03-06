#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from src.infrastructure.util import *

__author__ = 'qaqmander'


def get_inv_from_order_number_list(order_number_list):
    return list(map(lambda index: order_number_list.index(index), range(len(order_number_list))))


# return (lambda closure_table: lambda xs: [xs[index] for index in closure_table])(order_number_table.copy())
def get_map_from_order_number_table(order_number_table):
    return (lambda closure_table: lambda xs:
    list(map(lambda index: xs[closure_table[index]], range(len(closure_table)))))(
        order_number_table.copy())


def swap(bin_list):
    length = len(bin_list)
    return bin_list[length // 2:] + bin_list[:length // 2]


def xor(bin_list_0, bin_list_1):
    return list(map(lambda x, y: x ^ y, bin_list_0, bin_list_1))


def make_it_look_like_a_real_key_hex_str(fake_key_hex_str):
    fake_key = hex_str_to_bin_list(fake_key_hex_str, length=64)
    real_key = fake_key.copy()
    for i in range(8):
        xor_res = 0
        for j in range(7):
            xor_res ^= real_key[8 * i + j]
        real_key[8 * i + 7] = 1 - xor_res
    return bin_list_to_hex_str(real_key, length=16)


def output6(bin_list):
    length = len(bin_list)
    print([bin_list_to_num(bin_list[6 * i: 6 * (i + 1)]) for i in range(length // 6)])


def output4(bin_list):
    length = len(bin_list)
    print([bin_list_to_num(bin_list[4 * i: 4 * (i + 1)]) for i in range(length // 4)])


def get_everything_from_file(filename=r'DES.txt'):
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
