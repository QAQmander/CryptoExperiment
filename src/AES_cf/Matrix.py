#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from src.AES_cf.FiniteField import GF28Object, Polynomial2
from src.AES_cf.CompositeField import GF28Object_n, Polynomial_n, GF24Object_n, GF2Object_n


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


def fai(A, bin_list):
    new = A.mul(Matrix([bin_list]).translate())
    return new.translate().mat[0]


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


if __name__ == '__main__':
    print(GF28Object_n.from_ls([1, 1, 0, 1, 1]))
    ob28 = GF28Object(0b10010)
    ob242 = GF28Object_n([GF24Object_n.from_ls([1]), GF24Object_n.from_ls([1])])
    A = get_matrix(ob28, ob242)
    print(A)

