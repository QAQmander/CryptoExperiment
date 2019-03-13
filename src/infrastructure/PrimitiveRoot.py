#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import PrimeJudge
fermat = lambda x: PrimeJudge.fermat(x, 100)

def fai(p):
    ret = p
    for i in range(2, p + 1):
        if p % i == 0:
            ret -= ret // i
    return ret

def getPrimitiveRoot(p):
    '''
    if not fermat(p):
        print('Error : PrimitiveRoot.getPrimitiveRoot -- not prime')
        return None
    '''
    #faip = p - 1
    faip = fai(p)
    for i in range(2, p - 1):
        now = 1
        flag = True
        for j in range(1, faip):
            now = now * i % p
            if now == 1:
                flag = False
                break
        if flag:
            return i
    return None

if __name__ == '__main__':
    p = int(input())
    res = getPrimitiveRoot(p)
    if res:
        now = 1
        for i in range(p - 2):
            now = now * res % p
            print(now, end=' ')
        print()
    else:
        print('Error : no PrimitiveRoot for input')
