#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def bin_list_to_hex_str(bin_list, length):
    return hex(bin_list_to_num(bin_list))[2:].rjust(length, '0')


def hex_str_to_bin_list(hex_string, length):
    return num_to_bin_list(int(hex_string, 16), length)


def bin_list_to_num(bin_list):
    return int(''.join(map(str, bin_list)), 2)


def num_to_bin_list(num, length):
    return list(map(int, bin(num)[2:].rjust(length, '0')))

