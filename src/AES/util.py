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
