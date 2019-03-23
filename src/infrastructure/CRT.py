#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from src.infrastructure.Euclid import gcd_const  # request Euclid.py in same directory (used to)


def __reduce(f, init, a):  # general tool function
    # (int, int -> int), int, list -> int
    for i in a:
        init = f(init, i)
    return init


def __check(m_s):  # check if m[i] and m[j] are coprime for arbitrary i != j
    # list -> bool, int, int
    # ms -> flag, m[i], m[j]
    # flag represents whether m[i] and m[j] are coprime for arbitrary i != j
    # if flag == True, m[i] = m[j] = None; else m[i] and m[j] are not coprime
    length = len(m_s)
    for i in range(length):
        for j in range(length):
            if i != j and gcd_const(m_s[i], m_s[j])[2] != 1:  # judge if m[i] and m[j] are coprime
                return False, m_s[i], m_s[j]
    return True, None, None


def __calcM(m_s):  # calc M = m[0] * m[1] * ... * m[n - 1] using __reduce
    return __reduce(lambda x, y: x * y, 1, m_s)


def __calcc_s(m_s):  # calc c[i] = M[i] * (Invert(M[i])[mod m[i]]) % M
    # where M = m[0] * m[1] * ... * m[n - 1]
    #       M[i] = M // m[i]
    length = len(m_s)
    M = __calcM(m_s)  # calc M
    c_s = []
    for i in range(length):
        Mi = M // m_s[i]  # calc Mi
        MiImi = gcd_const(Mi, m_s[i])[0]  # calc Invert(M[i])[mod m[i]]
        ci = Mi * MiImi % M  # calc c[i]
        c_s.append(ci)
    return c_s


def CRT(m_s, a_s):  # Chinese Remainder Theorem
    # list, list -> int, int
    # m, a -> x, M (here require mi and mj are coprime)
    M = __calcM(m_s)  # calc M
    c_s = __calcc_s(m_s)  # calc c[i]
    ret = __reduce(lambda x, y: x + y, 0, \
                   map(lambda x, y: x * y, a_s, c_s))  # calc x = Sigma[0..(n-1)](c[i] * a[i])
    return ret % M, M


if __name__ == '__main__':
    print('Please input the numbers of equations first:')
    n = int(input())
    print('Please input mi in one line splited by space:')
    m_s = list(map(int, input().split()))

    flag, flagx, flagy = __check(m_s)  # check m
    if not flag:
        print('Maybe you should check mi more, ' \
              'esspecially these two: {} {}'.format(flagx, flagy))
        exit()

    print('Please input ai in one line splited by space:')
    a_s = list(map(int, input().split()))

    res, M = CRT(m_s, a_s)  # calc x and M using CRT
    print(res, M)
