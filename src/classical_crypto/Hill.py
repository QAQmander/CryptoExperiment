#!/usr/bin/env python3
# -*- coding: utf -*-

import sys
from fractions import Fraction

class matrix(object):

    def __init__(self, mat, n, m):
        self._n = n
        self._m = m 
        self._mat = [[None for j in range(m)] for i in range(n)]
        for i in range(n):
            for j in range(m):
                self._mat[i][j] = Fraction(mat[i][j], 1)

    def _row_swap(self, i, j):
        temp = self._mat[i]
        self._mat[i] = self._mat[j]
        self._mat[j] = temp

    def _row_times(self, i, k):
        self._mat[i] = list(map(lambda x: x * k, self._mat[i]))

    def _row_times_add(self, i, k, j):
        self._mat[j] = list(map(lambda x, y: k * x + y, \
                    self._mat[i], self._mat[j]))

    def __str__(self):
        ret = '%d %d\n' % (self._n, self._m)
        for i in range(self._n):
            ret += ' '.join(map(str, self._mat[i])) + '\n'
        return ret

    def row_reduce(self):
        for i in range(self._n):
            if self._mat[i][i] == 0:
                for j in range(i + 1, self._n):
                    if self._mat[i][j] != 0:
                        self._row_swap(i, j)
                        break
            if self._mat[i][i] == 0:
                print('Error : singular matrix')
                exit(-1)
            for j in range(self._n):
                if i != j:
                    self._row_times_add(j, \
                            -self._mat[i][i] / self._mat[j][j], i)

    @property
    def n(self):
        return self._n

    @property
    def m(self):
        return self._m

    @property
    def mat(self):
        return self._mat


def check(key):
    return True

def hill_encode(key, plain):
    m = key.get_m()
    length = len(plain)
    plain += 'x' * (m - (length - 1) % m - 1)
    length = len(plain)
    plain_block = []
    for i in range(length // m):
        plain_block.append(plain[m * i: m * (i + 1)])
    cipher_block = []
    for i in range(length // m):
        cipher_block.append(hill_encode_block(key, m))
    return ''.join(cipher_block)
    
def hill_decode(key, cipher):
    pass

if __name__ == '__main__':
    m = int(input('m: '))
    print('key matrix (m line, m items for each line):')
    key = []
    for i in range(m):
        key.append(list(map(int, input().split()))) 
    key = matrix(key, m)
    if not check(key):
        print('Error : key_matrix is not ok!!!')
        exit(-1)

    flag = sys.argv[1]
    if flag == '-e':
        plain = input('plain ([m]): ')
        print('cipher: ' + hill_encode(key, plain))
    elif flag == '-d':
        cipher = input('cipher ([c]): ')
        print('plain: ' + hill_decode(key, cipher))

