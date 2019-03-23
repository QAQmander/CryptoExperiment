#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'qaqmander'

from functools import reduce


def _bin_list_to_hex_str(bin_list, length):
    return hex(_bin_list_to_num(bin_list))[2:].rjust(length, '0')


def _hex_str_to_bin_list(hex_string, length):
    return _num_to_bin_list(int(hex_string, 16), length)


def _bin_list_to_num(bin_list):
    return int(''.join(map(str, bin_list)), 2)


def _num_to_bin_list(num, length):
    return list(map(int, bin(num)[2:].rjust(length, '0')))


def xor(bin_list_0, bin_list_1):
    return list(map(lambda x, y: x ^ y, bin_list_0, bin_list_1))


class DES(object):

    # to create closure without mutable arg object
    def __init__(self, ip, ip_inv, e, p, s, pc1, pc2, flag, s_box_input_length=6, s_box_output_length=4):

        # return (lambda closure_table: lambda xs: [xs[index] for index in closure_table])(order_number_table.copy())
        def get_map_from_order_number_table(order_number_table):
            return (lambda closure_table: lambda xs:
                    list(map(lambda index: xs[order_number_table[index]], range(len(order_number_table)))))(
                order_number_table.copy)

        self._ip = get_map_from_order_number_table(ip)
        if not ip_inv:
            ip_inv = list(map(lambda index: ip.index(index), range(len(ip))))
        self._ip_inv = get_map_from_order_number_table(ip_inv)
        self._e = get_map_from_order_number_table(e)
        self._p = get_map_from_order_number_table(p)
        self._temp_s = list(map(
            (lambda si:
             (lambda bin_list:
              ((lambda table_number: lambda bin_list_middle:
                _num_to_bin_list(
                    si[table_number * 2 ** s_box_output_length + _bin_list_to_num(bin_list_middle)],
                    length=s_box_output_length
                )
                )(_bin_list_to_num([bin_list[0], bin_list[-1]]))(bin_list[1:-1]))
              )
             ),
            map(lambda x: x.copy(), s)))
        self._s = lambda bin_list: reduce(
            lambda ls0, ls1: list.extend(ls0, ls1) or ls0,
            (lambda bin_list_slice_list: map(lambda func, x: func(x), self._temp_s, bin_list_slice_list))(
                (lambda func: lambda now_bin_list: func(func)(now_bin_list))(
                    lambda func: lambda now_bin_list:
                    [] if not now_bin_list
                    else [now_bin_list[:s_box_input_length]]
                         + func(func)(now_bin_list[s_box_input_length:])
                )(bin_list.copy())
            ),
            []
        )
        self._pc1 = get_map_from_order_number_table(pc1)
        self._pc2 = get_map_from_order_number_table(pc2)
        self._flag = (lambda closure_flag: lambda turn_number: closure_flag[turn_number])(flag) # unnecessary but cool
        self.__key = None    # SECRET!!!
        self._subkey_list = None

    def tell_me_the_devil_secret(self, key):
        self.__key = key

    def _calculate_subkey_list(self, turn):
        # print(self.__key)
        after_pc1 = self._pc1(self.__key)
        length = len(after_pc1)
        subkey_list = (lambda func: lambda now_subkey_lr: lambda turn_number: func(func)(now_subkey_lr)(turn_number)) \
            (lambda func: lambda now_subkey_lr: lambda turn_number:
                [] if turn_number == turn else
                (lambda next_subkey_lr:
                 [self._pc2(next_subkey_lr[0] + next_subkey_lr[1])] + func(func)(next_subkey_lr)(turn_number + 1))
                (tuple(map(
                    lambda key: ((key + key)[self._flag(turn_number):length // 2 + self._flag(turn_number)]),
                    now_subkey_lr
                )))
             )((after_pc1[:length // 2].copy(), after_pc1[length // 2:].copy()))(0)
        return subkey_list

    def _do_something_with_facilities(self, subkey_list, something_great, turn):
        length = len(something_great)
        after_ip = self._ip(something_great)
        # Y combinator with currying
        after_turns = (lambda func: lambda lr: lambda turn_number: func(func)(lr)(turn_number))(
            lambda func: lambda now_lr: lambda turn_number:
            now_lr if turn_number == turn
            else (lambda next_lr: lambda new_turn: func(func)(next_lr)(new_turn))
            ((now_lr[1], xor(now_lr[0],
                             (lambda bin_list: lambda subkey: self._p(self._s(xor(self._e(bin_list.copy()), subkey))))
                             (now_lr[1])
                             (subkey_list[turn_number])
                             )))(turn_number + 1)
        )((after_ip[:length // 2], after_ip[length // 2:]))(0)
        return self._ip_inv(after_turns[1] + after_turns[0])

    def encrypt(self, plain, turn=16):
        encrypt_subkey_list = self._calculate_subkey_list(turn)
        return self._do_something_with_facilities(encrypt_subkey_list, plain, turn)

    def decipher(self, cipher, turn=16):
        dicipher_subkey_list = self._calculate_subkey_list(turn)
        return self._do_something_with_facilities(dicipher_subkey_list.reverse() or dicipher_subkey_list, cipher, turn)


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
    everything = get_everything_from_file()
    des = DES(*everything)
    key_hex_str = r'133457799BBCDFF1'
    key = _hex_str_to_bin_list(key_hex_str, length=64)
    des.tell_me_the_devil_secret(key)
    plain_hex_str = r'0123456789ABCDEF'
    something_great = _hex_str_to_bin_list(plain_hex_str, length=64)
    print(_bin_list_to_hex_str(des.encrypt(something_great), length=16))
    cipher_hex_str = r'85e813540f0ab405'
    something_bad = _hex_str_to_bin_list(cipher_hex_str, length=64)
    print(_bin_list_to_hex_str(des.decipher(something_bad), length=16))
