# -*- coding: utf-8 -*-

"""
Now we get keccak_f and pad10_1 for other parts of sha3.
"""

import numpy as np
from math import log2

from src.sha3.keccak_and_pad import keccak_f, pad10_1

b = 1600
w = b // 25
l = int(log2(w))


class GoodException(Exception):
    def __init__(self, msg: np.ndarray) -> None:
        assert (msg.__class__ == np.ndarray)
        self.msg = msg

    def __str__(self) -> str:
        return self.msg.__str__()


# without type hint because I don't know
# how to describe type of function
def sponge(f, pad, r):
    """

    :param f: namely, keccak_f
    :param pad: namely, pad10_1
    :param r: 'the rate', namely b-c, namely 1600-c
    """

    def func(N: np.ndarray, d: int) -> np.ndarray:
        assert (len(N.shape) == 1)
        P = np.concatenate((N, pad(r, N.size)))
        n = P.size // r
        c = b - r
        p = []
        for i in range(n):
            p.append(P[r * i: r * (i + 1)])
        S = np.zeros((b,), dtype=int)
        for i in range(n):
            S = f(S ^ np.concatenate((p[i], np.zeros((c,), dtype=int))))
        try:
            Z = np.array([], dtype=int)
            while True:
                Z = np.concatenate((Z, S[:r]))
                if d < Z.size:
                    raise GoodException(Z[:d])
                S = f(S)
        except GoodException as e:
            return e.msg

    return func


def keccak(c: int):
    return sponge(keccak_f, pad10_1, b - c)


# M should be bit array
def sha3_224(M: np.ndarray) -> np.ndarray:
    assert (len(M.shape) == 1)
    for i in range(M.size):
        assert (M[i] in (0, 1))
    temp = np.concatenate((M, np.array([0, 1], dtype=int)))
    return keccak(448)(temp, 224)


def sha3_256(M: np.ndarray) -> np.ndarray:
    assert (len(M.shape) == 1)
    for i in range(M.size):
        assert (M[i] in (0, 1))
    temp = np.concatenate((M, np.array([0, 1], dtype=int)))
    return keccak(512)(temp, 256)


def sha3_384(M: np.ndarray) -> np.ndarray:
    assert (len(M.shape) == 1)
    for i in range(M.size):
        assert (M[i] in (0, 1))
    temp = np.concatenate((M, np.array([0, 1], dtype=int)))
    return keccak(768)(temp, 384)


def sha3_512(M: np.ndarray) -> np.ndarray:
    assert (len(M.shape) == 1)
    for i in range(M.size):
        assert (M[i] in (0, 1))
    temp = np.concatenate((M, np.array([0, 1], dtype=int)))
    return keccak(1024)(temp, 512)


def output(a: np.ndarray) -> None:
    assert (len(a.shape) == 1)
    assert (a.size % 8 == 0)
    for i in range(a.size // 8):
        now_mes = ''.join(map(str, a[8 * i: 8 * (i + 1)]))[::-1]
        now = int(now_mes, 2)
        print(hex(now)[2:].rjust(2, '0'), end=' ')
        if i % 16 == 15:
            print()


if __name__ == '__main__':
    a = [1, 1, 0, 0, 0, 1, 0, 1] * 200
    a = np.array(a)
    b = sha3_224(a)
    output(b)
