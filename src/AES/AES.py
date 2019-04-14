#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from src.infrastructure.util import *
from src.infrastructure.FiniteField import GF28Object
from src.AES.util import *


class AES(object):

    def __init__(self, s, s_inv, rc, column_mix, column_mix_inv):
        self.src_s = []
        for item in s:
            self.src_s.append(item.copy())
        self.src_s_inv = []
        for item in s_inv:
            self.src_s_inv.append(item.copy())
        self.src_rc = rc.copy()
        self.src_cm = []
        for item in column_mix:
            self.src_cm.append(item.copy())
        self.src_cm_inv = []
        for item in column_mix_inv:
            self.src_cm_inv.append(item.copy())
        self.__key = None
        self.subkey_list = None
        self._cm_matrix = []
        for i in range(4):
            self._cm_matrix.append([])
            for j in range(4):
                self._cm_matrix[i].append(GF28Object(self.src_cm[i][j]))
        self._cm_matrix_inv = []
        for i in range(4):
            self._cm_matrix_inv.append([])
            for j in range(4):
                self._cm_matrix_inv[i].append(GF28Object(self.src_cm_inv[i][j]))

    def tell_me_the_devil_secret(self, key):
        self.__key = bin_list_to_byte_list(key.copy())

    def forget_the_devil_secret(self):
        self.__key = None

    def encrypt(self, plain):
        now = bin_list_to_byte_list(plain.copy())
        self._calculate_subkey_list()
        now = self._subkey_add(now, self.subkey_list[0])
        for i in range(1, 10):
            now = self._do_one_turn(now, self.subkey_list[i])
        now = self._byte_substitute(now)
        now = self._row_shift(now)
        now = self._subkey_add(now, self.subkey_list[10])
        return byte_list_to_bin_list(now)

    def decrypt(self, cipher):
        now = bin_list_to_byte_list(cipher.copy())
        self._calculate_subkey_list()
        now = self._subkey_add(now, self.subkey_list[10])
        for i in range(9, 0, -1):
            now_subkey = self._column_mix(self.subkey_list[i], reverse=True)
            now = self._do_one_turn(now, now_subkey, reverse=True)
        now = self._row_shift(now, reverse=True)
        now = self._byte_substitute(now, reverse=True)
        now = self._subkey_add(now, self.subkey_list[0])
        return byte_list_to_bin_list(now)

    def _calculate_subkey_list(self):
        self.subkey_list = [self.__key]
        for i in range(10):
            after_g = self._g(self.subkey_list[i][12:16], i)
            now = []
            for k in range(4):
                now.append(self.subkey_list[i][k] ^ after_g[k])
            for j in range(3):
                for k in range(4):
                    now.append(self.subkey_list[i][4 * j + k + 4] ^ now[4 * j + k])
            self.subkey_list.append(now)

    def _g(self, byte_4_list, turn_number):
        new_byte_4_list = [byte_4_list[1], byte_4_list[2], byte_4_list[3], byte_4_list[0]]
        for i in range(len(new_byte_4_list)):
            new_byte_4_list[i] = self._s(new_byte_4_list[i])
        new_byte_4_list[0] ^= self.src_rc[turn_number]
        return new_byte_4_list

    def _s(self, byte):
        high = byte // 16
        low = byte % 16
        return self.src_s[high][low]

    def _s_inv(self, byte):
        high = byte // 16
        low = byte % 16
        return self.src_s_inv[high][low]

    def _do_one_turn(self, passed, subkey, reverse=False):
        now = self._byte_substitute(passed, reverse)
        now = self._row_shift(now, reverse)
        now = self._column_mix(now, reverse)
        now = self._subkey_add(now, subkey)
        return now

    def _byte_substitute(self, passed, reverse=False):
        _s = self._s if not reverse else self._s_inv
        now = []
        for i in range(len(passed)):
            now.append(_s(passed[i]))
        return now

    @staticmethod
    def _row_shift(passed, reverse=False):
        if not reverse:
            return [
                passed[0], passed[5], passed[10], passed[15],
                passed[4], passed[9], passed[14], passed[3],
                passed[8], passed[13], passed[2], passed[7],
                passed[12], passed[1], passed[6], passed[11],
            ]
        else:
            return [
                passed[0], passed[13], passed[10], passed[7],
                passed[4], passed[1], passed[14], passed[11],
                passed[8], passed[5], passed[2], passed[15],
                passed[12], passed[9], passed[6], passed[3]
            ]

    @staticmethod
    def _matrix_mul(matrix, column):
        ret = [GF28Object(0), GF28Object(0), GF28Object(0), GF28Object(0)]
        for j in range(4):
            for k in range(4):
                ret[j] = ret[j].add(column[k].mul(matrix[j][k]))
        ret = list(map(int, ret))
        return ret

    def _column_mix(self, passed, reverse=False):
        matrix = self._cm_matrix if not reverse else self._cm_matrix_inv
        now = []
        for i in range(4):
            column = list(map(lambda item: GF28Object(item), passed[4 * i: 4 * i + 4]))
            now += AES._matrix_mul(matrix, column)
        return now

    def _subkey_add(self, passed, subkey):
        now = []
        for i in range(len(passed)):
            now.append(passed[i] ^ subkey[i])
        return now


def get_everything_from_file(filename=r'AES.txt'):
    s = []
    s_inv = []
    rc = []
    column_mix = []
    column_mix_inv = []
    with open(filename, 'r') as fr:
        fr.readline()
        for i in range(16):
            line = fr.readline().strip().split()
            line = list(map(lambda x: int(x, 16), line))
            s.append(line)
        fr.readline()
        print()
        for i in range(16):
            line = fr.readline().strip().split()
            line = list(map(lambda x: int(x, 10), line))
            s_inv.append(line)
        fr.readline()
        line = fr.readline().strip().split()
        line = list(map(lambda x: int(x, 16), line))
        rc = line
        fr.readline()
        for i in range(4):
            line = fr.readline().strip().split()
            line = list(map(lambda x: int(x, 16), line))
            column_mix.append(line)
        fr.readline()
        for i in range(4):
            line = fr.readline().strip().split()
            line = list(map(lambda x: int(x, 16), line))
            column_mix_inv.append(line)
    return s, s_inv, rc, column_mix, column_mix_inv


if __name__ == '__main__':
    everything = get_everything_from_file()
    aes = AES(*everything)
    print(num_to_bin_list(aes._s(10), length=8))
    exit(0)
    # key = hex_str_to_byte_list(r"2b7e151628aed2a6abf7158809cf4f3c")
    # plain = hex_str_to_byte_list(r"3243f6a8885a308d313198a2e0370734")
    # key = hex_str_to_bin_list(r'0f1571c947d9e8590cb7add6af7f6798', length=128)
    # plain = hex_str_to_bin_list(r'0123456789abcdeffedcba9876543210', length=128)
    key = hex_str_to_bin_list(r'cafebabecafebabecafebabecafebabe', length=128)
    plain = hex_str_to_bin_list(r'deadbeefdeadbeefdeadbeefdeadbeef', length=128)
    aes.tell_me_the_devil_secret(key)
    cipher = aes.encrypt(plain)
    new_plain = aes.decrypt(cipher)
    print('             key: ', end='')
    byte_list_output(bin_list_to_byte_list(key))
    print('           plain: ', end='')
    byte_list_output(bin_list_to_byte_list(plain))
    print('after encrypting: ', end='')
    byte_list_output(bin_list_to_byte_list(cipher))
    print('after decrypting: ', end='')
    byte_list_output(bin_list_to_byte_list(new_plain))
