#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from src.infrastructure.util import *


def hex_str_to_byte_list(hex_str, length=16):
    bin_list = hex_str_to_bin_list(hex_str, length=length * 8)
    ret = []
    for i in range(length):
        ret.append(bin_list_to_num(bin_list[8 * i: 8 * (i + 1)]))
    return ret


def byte_list_output(byte_list):
    temp = list(map(lambda x: '{:0>2}'.format(hex(x)[2:]), byte_list))
    print(' '.join(temp))


def byte_list_to_hex_str(byte_list):
    return ''.join(map(lambda x: '{:0>2}'.format(hex(x)[2:]), byte_list))


def byte_list_to_bin_list(byte_list):
    temp = []
    for byte in byte_list:
        temp += list(map(int, '{:0>8}'.format(bin(byte)[2:])))
    return temp


def bin_list_to_byte_list(bin_list):
    temp = []
    for i in range(len(bin_list) // 8):
        temp.append(int(''.join(map(str, bin_list[8 * i: 8 * (i + 1)])), 2))
    return temp


def byte_list_to_num(byte_list):
    return bin_list_to_num(byte_list_to_bin_list(byte_list))


def xor(bin_list_1, bin_list_2):
    length = max(len(bin_list_1), len(bin_list_2))
    ret = [0] * length
    for i in range(len(bin_list_1)):
        try:
            ret[i] = bin_list_1[i] ^ bin_list_2[i]
        except IndexError:
            break
    return ret
