#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from fractions import Fraction
from src.infrastructure.Euclid import inv, gcd
from random import sample


class Matrix(object):

    def __init__(self, mat):
        self._n = len(mat)
        self._m = len(mat[0])
        self._mat = [[None for j in range(self._m)] for i in range(self._n)]
        for i in range(self._n):
            for j in range(self._m):
                self._mat[i][j] = Fraction(mat[i][j])

    def _row_swap(self, i, j):  # swap two lines
        temp = self._mat[i]
        self._mat[i] = self._mat[j]
        self._mat[j] = temp

    def _row_times(self, i, k):  # multiply one line by a num
        self._mat[i] = list(map(lambda x: x * k, self._mat[i]))

    def _row_times_add(self, i, k, j):  # multiply one line by a num then add to other line
        self._mat[j] = list(map(lambda x, y: k * x + y, self._mat[i], self._mat[j]))

    def __str__(self):
        ret = '%d %d\n' % (self._n, self._m)
        for i in range(self._n):
            ret += ' '.join(map(str, self._mat[i])) + '\n'
        return ret

    def __repr__(self):
        return self.__str__()

    def row_reduce(self):  # without transforming to all ones
        for i in range(self._n):
            if self._mat[i][i] == 0:
                for j in range(i + 1, self._n):
                    if self._mat[j][i] != 0:
                        self._row_swap(i, j)
                        break
            if self._mat[i][i] == 0:
                print('Error : Hill.Matrix.row_reduce -- singular matrix')
                exit(-1)
            for j in range(self._n):
                if i != j:
                    self._row_times_add(i, -self._mat[j][i] / self._mat[i][i], j)
        return self

    def _row_reduce_one(self):  # help looking for inv
        self.row_reduce()
        one = Fraction(1, 1)
        for i in range(self._n):
            if self._mat[i][i] != one:
                self._row_times(i, one / self._mat[i][i])
        return self

    def copy(self):
        new_mat = []
        for i in range(self._n):
            new_mat.append(self._mat[i].copy())
        return Matrix(new_mat)

    def determinant(self):
        if self._n != self._m:
            print('Error : Hill.Matrix.determinant -- not square matrix')
            exit(-1)
        other = self.copy()
        other.row_reduce()
        res = Fraction(1, 1)
        for i in range(self._n):
            res *= self._mat[i][i]
        return res

    def inv(self):
        if self._n != self._m:
            print('Error : Hill.Matrix.inv -- not square matrix')
        det = self.determinant()
        if det == 0:
            print('Error : Hill.Matrix.inv -- not invertible')
        nowmat = self.copy()._mat
        for i in range(self._n):
            for j in range(self._n):
                if i == j:
                    nowmat[j].append(Fraction(1, 1))
                else:
                    nowmat[j].append(Fraction(0, 1))
        nowmat = Matrix(nowmat)._row_reduce_one()
        ret = []
        for i in range(self._n):
            ret.append(nowmat._mat[i][self._n:])
        return Matrix(ret)

    def mul(self, other):
        if self._m != other._n:
            print('Error : Hill.Matrix.mul -- self._m == other._n required')
            exit(-1)
        n, m, p = self._n, self._m, other._m
        mat = [[Fraction(0, 1) for j in range(p)] for i in range(n)]
        for i in range(n):
            for j in range(p):
                for k in range(m):
                    mat[i][j] += self._mat[i][k] * other._mat[k][j]
        return Matrix(mat)

    def to_mod26(self):
        now_mat = [[0 for j in range(self._m)] for i in range(self._n)]
        for i in range(self._n):
            for j in range(self._m):
                now_mat[i][j] = self._mat[i][j].numerator * \
                                inv(self._mat[i][j].denominator, 26) % 26
        return now_mat

    @property
    def n(self):
        return self._n

    @property
    def m(self):
        return self._m

    @property
    def mat(self):
        return self._mat


def check(key):  # check if det(key) and 26 are coprime
    det = int(key.determinant())
    if gcd(det, 26).d != 1:
        return False
    else:
        return True


def hill_encode_block(key, plain_block):  # matrix multiplication
    vector = []
    for char in plain_block:
        vector.append([ord(char) - ord('a')])
    res_matrix = key.mul(Matrix(vector)).to_mod26()
    return ''.join(map(lambda x: chr(x[0] + ord('a')), res_matrix))


def hill_encode(key, plain):
    m = key.m
    length = len(plain)
    plain += 'x' * (m - (length - 1) % m - 1)
    length = len(plain)
    plain_blocks = []
    for i in range(length // m):
        plain_blocks.append(plain[m * i: m * (i + 1)])
    cipher_blocks = []
    for i in range(length // m):
        cipher_blocks.append(hill_encode_block(key, plain_blocks[i]))
    return ''.join(cipher_blocks)


def hill_decode_block(key, cipher_block):  # inv then matrix multiplication
    key_inv = key.inv()
    vector = []
    for char in cipher_block:
        vector.append([ord(char) - ord('a')])
    res_matrix = key_inv.mul(Matrix(vector)).to_mod26()
    return ''.join(map(lambda x: chr(x[0] + ord('a')), res_matrix))


def hill_decode(key, cipher):
    m = key.m
    length = len(cipher)
    if length % m != 0:
        print('Error : Hill.hill_decode -- cipher % m != 0')
    plain_blocks = []
    for i in range(length // m):
        plain_blocks.append(hill_decode_block(key, cipher[m * i: m * (i + 1)]))
    return ''.join(plain_blocks)


def attack(plain, cipher):
    length = len(plain)
    plain += 'x' * (m - (length - 1) % m - 1)
    length = len(plain)

    plain_blocks = []
    cipher_blocks = []
    for i in range(length // m):
        plain_blocks.append(plain[m * i: m * (i + 1)])
        cipher_blocks.append(cipher[m * i: m * (i + 1)])

    tot = 0
    while True:
        tot += 1
        if tot == 1000000:
            print('Error : Hill.attach -- something wrong')
            exit(-1)
        ls = sample(range(0, length // m), m)
        mat = []
        for i in range(m):
            mat.append(list(map(lambda x: ord(plain_blocks[x][i]) - ord('a'), ls)))
        mat = Matrix(mat)
        if check(mat):
            res = []
            for i in range(m):
                res.append(list(map(lambda x: ord(cipher_blocks[x][i]) - ord('a'), ls)))
            res = Matrix(res)
            # print(mat)
            # print(res)
            key = Matrix(res.mul(mat.inv()).to_mod26())
            if hill_encode(key, plain) == cipher:
                return key


if __name__ == '__main__':
    flag = input('flag: ')
    m = int(input('m: '))
    if flag != '-a':
        print('key matrix (m line, m items for each line):')
        key = []
        for i in range(m):
            key.append(list(map(int, input().split())))
        key = Matrix(key)
        if not check(key):
            print('Error : Hill -- key_matrix is not ok!!!')
            exit(-1)

    # flag = sys.argv[1]
    if flag == '-e':
        plain = input('plain ([m]): ')
        print('cipher: ' + hill_encode(key, plain))
    elif flag == '-d':
        cipher = input('cipher ([c]): ')
        print('plain: ' + hill_decode(key, cipher))
    elif flag == '-a':
        plain = input('plain ([m]): ')
        cipher = input('cipher ([c]): ')
        key = attack(plain, cipher)
        print(key)
