#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from src.AES_cf.FiniteField import GF28Object, Polynomial2
from src.AES_cf.CompositeField import GF28Object_n, Polynomial_n, GF24Object_n, GF2Object_n
from src.infrastructure.util import *


class Matrix(object):

    def __init__(self, mat):
        self.n = len(mat)
        self.m = len(mat[0])
        self.mat = [[0 for j in range(self.m)] for i in range(self.n)]
        for i in range(self.n):
            for j in range(self.m):
                self.mat[i][j] = mat[i][j]

    def _row_swap(self, i, j):  # swap two lines
        temp = self.mat[i]
        self.mat[i] = self.mat[j]
        self.mat[j] = temp

    def _row_times(self, i, k):  # multiply one line by a num
        self.mat[i] = list(map(lambda x: x & k, self.mat[i]))

    def _row_add(self, i, j):  # multiply one line by a num then add to other line
        self.mat[j] = list(map(lambda x, y: x ^ y, self.mat[i], self.mat[j]))

    def __str__(self):
        ret = '%d %d\n' % (self.n, self.m)
        for i in range(self.n):
            ret += ' '.join(map(str, self.mat[i])) + '\n'
        return ret

    def __repr__(self):
        return self.__str__()

    def row_reduce(self):  # without transforming to all ones
        for i in range(self.n):
            if self.mat[i][i] == 0:
                for j in range(i + 1, self.n):
                    if self.mat[j][i] != 0:
                        self._row_swap(i, j)
                        break
            if self.mat[i][i] == 0:
                print('Error : Matrix.Matrix.row_reduce -- singular matrix')
                exit(-1)
            for j in range(self.n):
                if i != j and self.mat[j][i] == 1:
                    self._row_add(i, j)
        return self

    def copy(self):
        return Matrix(self.mat)

    def inv(self):
        if self.n != self.m:
            print('Error : Hill.Matrix.inv -- not square matrix')
        nowmat = self.copy().mat
        for i in range(self.n):
            for j in range(self.n):
                if i == j:
                    nowmat[j].append(1)
                else:
                    nowmat[j].append(0)
        nowmat = Matrix(nowmat).row_reduce()
        ret = []
        for i in range(self.n):
            ret.append(nowmat.mat[i][self.n:])
        return Matrix(ret)

    def mul(self, other):
        if self.m != other.n:
            print('Error : Matrix.Matrix.mul -- self._m == other._n required')
            exit(-1)
        n, m, p = self.n, self.m, other.m
        mat = [[0 for j in range(p)] for i in range(n)]
        for i in range(n):
            for j in range(p):
                for k in range(m):
                    mat[i][j] ^= self.mat[i][k] * other.mat[k][j]
        return Matrix(mat)

    def translate(self):
        mat = [[self.mat[j][i] for j in range(self.n)] for i in range(self.m)]
        return Matrix(mat)


def fai(A: Matrix, bin_list: list) -> list:
    new = A.mul(Matrix([bin_list]).translate())
    return new.translate().mat[0]


def good_fai(A: Matrix, ob28: GF28Object) -> GF28Object_n:
    bin_list = ob28.to_bin_list()
    y = fai(A, bin_list)
    return GF28Object_n.from_ls(y)


def bad_fai(A: Matrix, ob242: GF28Object_n) -> GF28Object:
    bin_list = ob242.to_bin_list()
    y = fai(A.inv(), bin_list)
    return GF28Object(bin_list_to_num(y))


def ok_ma(A: Matrix, ob28: GF28Object, ob242: GF28Object_n) -> bool:
    ob28_bin_list = ob28.to_bin_list()
    ob242_bin_list = ob242.to_bin_list()
    # print(fai(A, ob28_bin_list))
    # print(ob242_bin_list)
    return eq(fai(A, ob28_bin_list), ob242_bin_list)


def eq(binlist1, binlist2):
    for i in range(len(binlist1)):
        if binlist1[i] != binlist2[i]:
            return False
    return True


def get_matrix(ob28, ob242):
    x = []
    now = GF28Object(1)
    for i in range(8):
        x.append(now.to_bin_list())
        now = now.mul(ob28)
    y = []
    now = GF28Object_n([GF24Object_n.from_ls([1])])
    for i in range(8):
        y.append(now.to_bin_list())
        now = now * ob242
    x = Matrix(x)
    y = Matrix(y)
    return x.inv().mul(y).translate()


def show_isomorphic_map():
    import pickle
    with open('pr242', 'rb') as fr:
        pr242_ls = pickle.load(fr)
    with open('pr28', 'rb') as fr:
        pr28_ls = pickle.load(fr)

    pr242_binlist_ls = []
    for i in pr242_ls:
        pr242_binlist_ls.append(i.to_bin_list())

    ob28_one = GF28Object(1)
    ob242_one = GF28Object_n([GF24Object_n.from_ls([1])])
    for i in pr28_ls:
        for j in pr242_ls:
            ob28 = i
            ob242 = j
            A = get_matrix(ob28, ob242)
            # print(fai(ob28.to_bin_list()))
            # print(ob242.to_bin_list())
            # print(eq(fai(ob28.to_bin_list()), ob242.to_bin_list()))
            ob28_now = ob28_one
            ob242_now = ob242_one
            flag = True
            for j in range(255):
                addone28 = ob28_now.add(ob28_one)
                addone242 = ob242_now + ob242_one
                if not eq(fai(A, addone28.to_bin_list()), addone242.to_bin_list()):
                    flag = False
                    break
                ob28_now = ob28_now.mul(ob28)
                ob242_now = ob242_now * ob242
            if flag:
                print(ob28)
                print(ob242)
                print(flag)
                print(A)


def test(A):

    for i in range(1 << 8):
        ob28_1 = GF28Object(i)
        ob28_2 = GF28Object(0b1)
        ob242_1 = good_fai(A, ob28_1)
        ob242_2 = good_fai(A, ob28_2)

        ob28_add = ob28_1.add(ob28_2)
        ob242_add = ob242_1 + ob242_2

        if not ok_ma(A, ob28_add, ob242_add):
            print(ob28_1)
            print(ob28_2)
            return False
    print('ADD: success')

    for i in range(1 << 8):
        ob28_1 = GF28Object(i)
        ob28_2 = GF28Object(0b10010)
        ob242_1 = good_fai(A, ob28_1)
        ob242_2 = good_fai(A, ob28_2)

        ob28_mul = ob28_1.mul(ob28_2)
        ob242_mul = ob242_1 * ob242_2

        if not ok_ma(A, ob28_mul, ob242_mul):
            print(ob28_1)
            print(ob28_2)
            return False
    print('MUL: success')

    return True


'''
A:
8 8
1 0 1 0 1 1 0 0
1 1 0 1 1 1 1 0
1 1 0 1 0 0 1 0
0 1 1 1 1 1 0 0
1 0 0 0 1 1 0 0
1 0 0 1 0 0 1 0
1 0 1 0 0 1 0 0
1 0 0 1 1 0 0 1

A.inv():
8 8
0 1 1 0 1 0 0 0
0 0 1 0 0 1 0 0
1 0 0 0 1 0 0 0
1 1 0 1 1 1 0 0
1 0 0 0 0 0 1 0
1 1 1 0 0 0 1 0
1 0 1 1 0 0 0 0
0 0 1 1 0 1 1 1
'''
ob28 = GF28Object(0b10010)
ob242 = GF28Object_n([GF24Object_n.from_ls([1]), GF24Object_n.from_ls([1])])
A = get_matrix(ob28, ob242)
if __name__ == '__main__':
    from src.infrastructure.util import *
    # [2, 7, 0, 5, 6, 3, 4, 1, 10, 15, 8, 13, 14, 11, 12, 9]
    B = [
        [GF28Object(0x02), GF28Object(0x03), GF28Object(0x01), GF28Object(0x01)],
        [GF28Object(0x01), GF28Object(0x02), GF28Object(0x03), GF28Object(0x01)],
        [GF28Object(0x01), GF28Object(0x01), GF28Object(0x02), GF28Object(0x03)],
        [GF28Object(0x03), GF28Object(0x01), GF28Object(0x01), GF28Object(0x02)]
    ]
    B_inv = [
        [GF28Object(0x0E), GF28Object(0x0B), GF28Object(0x0D), GF28Object(0x09)],
        [GF28Object(0x09), GF28Object(0x0E), GF28Object(0x0B), GF28Object(0x0D)],
        [GF28Object(0x0D), GF28Object(0x09), GF28Object(0x0E), GF28Object(0x0B)],
        [GF28Object(0x0B), GF28Object(0x0D), GF28Object(0x09), GF28Object(0x0E)]
    ]
    for i in range(len(B_inv)):
        for j in range(len(B_inv[i])):
            B_inv[i][j] = good_fai(A, B_inv[i][j])
    for i in B_inv:
        for j in i:
            print('0x' + bin_list_to_hex_str(j.to_bin_list(), length=2), end=' ')
        print()
    exit(0)
    C = [[0, 4, 8, 12], [1, 5, 9, 13], [2, 6, 10, 14], [3, 7, 11, 15]]
    for i in range(4):
        for j in range(4):
            C[i][j] = good_fai(A, GF28Object(C[i][j]))
    print()
    for i in C:
        for j in i:
            print(j.to_hex_str(), end=' ')
        print()
    D = [[0] * 4 for i in range(4)]
    for i in range(4):
        for j in range(4):
            D[i][j] = GF28Object_n.from_num(D[i][j])
    for i in range(4):
        for j in range(4):
            for k in range(4):
                D[i][j] += B[i][k] * C[k][j]
    print()
    for i in D:
        for j in i:
            print(j.to_hex_str(), end=' ')
        print()

    for i in range(4):
        for j in range(4):
            D[i][j] = bad_fai(A, D[i][j])
    print()
    for i in D:
        for j in i:
            print(j._poly._poly, end=' ')
        print()
    '''
    B = Matrix([
        [1, 1, 1, 1, 1, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 0, 0],
        [0, 0, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1, 1, 1, 1],
        [1, 1, 0, 0, 0, 1, 1, 1],
        [1, 1, 1, 0, 0, 0, 1, 1],
        [1, 1, 1, 1, 0, 0, 0, 1]
    ])
    B = B.inv()
    C = A.mul(B).mul(A.inv())
    print(C)
    a = []
    for i in C.mat:
        a.append(bin_list_to_hex_str(i, length=2))
    print('HAH-1', ', 0x'.join(a))
    # D = [0, 1, 1, 0, 0, 0, 1, 1]
    D = [0, 0, 0, 0, 0, 1, 0, 1]
    E = A.mul(Matrix([D]).translate())
    print('B:', bin_list_to_hex_str(E.translate().mat[0], length=2))

    start = GF28Object(0x95)
    start = num_to_bin_list(start.inv()._poly._poly, length=8)
    print('inv:', start)
    start = B.mul(Matrix([start]).translate()).translate().mat[0]
    print('mul:', start)
    for i in range(8):
        start[i] = start[i] ^ D[i]
    print(start)
    '''
    '''
    ob28 = GF28Object(0b10010)
    ob242 = GF28Object_n([GF24Object_n.from_ls([1]), GF24Object_n.from_ls([1])])
    A = get_matrix(ob28, ob242)
    for i in range(0xff + 1):
        x = GF28Object(i)
        print(bin_list_to_hex_str(good_fai(A.inv(), x).to_bin_list(), length=2))
    '''
    '''
    # print(GF28Object_n.from_ls([1, 1, 0, 1, 1]))
    print(A)
    mat = A.mat
    for i in mat:
        print(bin_list_to_hex_str(i, length=2))
    print(A.inv())
    mat = A.inv().mat
    for i in mat:
        print(bin_list_to_hex_str(i, length=2))
    # print(test(A))
    '''
