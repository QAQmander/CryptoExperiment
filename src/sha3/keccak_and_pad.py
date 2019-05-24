# -*- coding: utf-8 -*-

"""
  This python file provides keccak_f and pad functinos for
other modules to use, which is specified in chapter 3.2.
  Input and output of each function is state array, repre-
sented as np.ndarray, with b = 1600 always.
"""

import numpy as np
from math import log2

b = 1600
w = b // 25
l = int(log2(w))


def to_statearray(S: np.ndarray) -> np.ndarray:
    assert (S.__class__ == np.ndarray)
    assert (S.shape == (b,))
    temp = np.reshape(S, newshape=(5, 5, w))
    A = np.transpose(temp, axes=(1, 0, 2))
    assert (A.shape == (5, 5, w))
    return A


def from_statearray(A: np.ndarray) -> np.ndarray:
    assert (A.__class__ == np.ndarray)
    assert (A.shape == (5, 5, w))
    temp = np.transpose(A, axes=(1, 0, 2))
    S = np.reshape(temp, newshape=(b,))
    assert (S.shape == (b,))
    return S


def theta(A: np.ndarray) -> np.ndarray:
    assert (A.__class__ == np.ndarray)
    assert (A.shape == (5, 5, w))
    C = A[:, 0, :] ^ A[:, 1, :] ^ A[:, 2, :] ^ A[:, 3, :] ^ A[:, 4, :]
    D = np.roll(C, shift=1, axis=0) ^ np.roll(C, shift=(-1, 1), axis=(0, 1))
    A_ = A ^ np.repeat(D[:, None, :], repeats=5, axis=1)
    assert (A_.shape == (5, 5, w))
    return A_


def rho(A: np.ndarray) -> np.ndarray:
    assert (A.__class__ == np.ndarray)
    assert (A.shape == (5, 5, w))
    # A_ = A.copy()
    A_ = np.zeros((5, 5, w), dtype=int)
    A_[0, 0, :] = A[0, 0, :]
    x, y = 1, 0
    for t in range(0, 23 + 1):
        A_[x, y, :] = np.roll(A[x, y, :], shift=(t + 1) * (t + 2) // 2)
        x, y = y, (2 * x + 3 * y) % 5
    assert (A_.shape == (5, 5, w))
    return A_


def pi(A: np.ndarray) -> np.ndarray:
    assert (A.__class__ == np.ndarray)
    assert (A.shape == (5, 5, w))
    A_ = np.zeros((5, 5, w), dtype=int)
    for x in range(5):
        for y in range(5):
            A_[x, y, :] = A[(x + 3 * y) % 5, x, :]
    assert (A_.shape == (5, 5, w))
    return A_


def chi(A: np.ndarray) -> np.ndarray:
    assert (A.__class__ == np.ndarray)
    assert (A.shape == (5, 5, w))
    temp = np.roll(A, shift=-1, axis=0) ^ np.ones(A.shape, dtype=int)
    temp = temp & np.roll(A, shift=-2, axis=0)
    A_ = A ^ temp
    assert (A_.shape == (5, 5, w))
    return A_


'''
def rc(t):
    if t % 255 == 0:
        return 1
    else:
        R = [1, 0, 0, 0, 0, 0, 0, 0]
        for i in range(1, t % 255 + 1):
            R = [0] + R
            R[0] = R[0] ^ R[8]
            R[4] = R[4] ^ R[8]
            R[5] = R[5] ^ R[8]
            R[6] = R[6] ^ R[8]
            R = R[:8]
        return R[0]

rc_array = []
for i in range(255):
    rc_array.append(rc(i))
# we get rc_array
'''
rc_array = np.array(
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1,
     1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0,
     0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0,
     0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1,
     1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1,
     0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1,
     0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0,
     1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0])


def iota(A: np.ndarray, ir: int) -> np.ndarray:
    assert (A.__class__ == np.ndarray)
    assert (A.shape == (5, 5, w))
    RC = np.zeros((w,), dtype=int)
    for j in range(0, l + 1):
        RC[2 ** j - 1] = rc_array[(j + 7 * ir) % 255]
    A_ = A.copy()
    A_[0, 0, :] = A_[0, 0, :] ^ RC
    assert (A_.shape == (5, 5, w))
    return A_


def rnd(A: np.ndarray, ir: int) -> np.ndarray:
    assert (A.__class__ == np.ndarray)
    assert (A.shape == (5, 5, w))
    return iota(chi(pi(rho(theta(A)))), ir)


def keccak_p(S: np.ndarray, nr: int) -> np.ndarray:
    assert (S.__class__ == np.ndarray)
    assert (S.shape == (b,))
    A = to_statearray(S)
    for ir in range(12 + 2 * l - nr, 12 + 2 * l - 0):
        A = rnd(A, ir)
    S_ = from_statearray(A)
    assert (S_.shape == (b,))
    return S_


def keccak_f(S: np.ndarray) -> np.ndarray:
    assert (S.__class__ == np.ndarray)
    assert (S.shape == (b,))
    S_ = keccak_p(S, 12 + 2 * l)
    assert (S_.shape == (b,))
    return S_


# for test
def output(A: np.ndarray) -> None:
    if A.shape == (b,):
        for i in range(len(A) // 8):
            now_mes = ''.join(map(str, A[8 * i: 8 * (i + 1)]))[::-1]
            now = int(now_mes, 2)
            print(hex(now)[2:].rjust(2, '0') + ' ', end='')
            if i % 16 == 15:
                print()
        print()
    else:
        assert (A.shape == (5, 5, w))
        A_ = from_statearray(A)
        output(A_)


def pad10_1(x: int, m: int) -> np.ndarray:
    j = (- m - 2) % x
    return np.array([1] + [0] * j + [1])


if __name__ == '__main__':
    a = [1, 1, 0, 0, 0, 1, 0, 1] * (16 * 9) + [0, 0, 0, 0, 0, 0, 0, 0] * 56
    a = np.array(a)
    c = keccak_f(a)
    output(c)
