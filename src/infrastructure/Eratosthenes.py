#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def era_recursive(n):  # recursive, int -> list
    if n <= 10:  # if n < 10, get answer directly
        return list(filter(lambda x: x <= n, [2, 3, 5, 7]))
    primes = era_recursive(int(n ** 0.5))  # get primes below sqrt(n)
    ret = list(range(2, n + 1))
    for prime in primes:  # filter composite numbers
        ret = list(filter(lambda x: x % prime != 0 or x == prime, ret))
    return ret


def era_iterative(n):  # iterative, improved, int -> list
    # exchange space for time
    flag = [True for i in range(n + 1)]
    flag[0] = False
    flag[1] = False
    i = 2
    while i * i <= n:  # only use primes below sqrt(n)
        if flag[i]:
            j = i * i  # filter beginning with i * i
            while j <= n:
                flag[j] = False
                j += i  # increase by i each time
        i += 1
    return list(filter(lambda x: flag[x], range(n + 1)))
    # return primes according to flags


if __name__ == '__main__':
    n = int(input())
    if n <= 0:  # for robustness
        print('n should be positive!')
    else:
        res = era_iterative(n)
        for num in res:
            print(num, end=' ')
