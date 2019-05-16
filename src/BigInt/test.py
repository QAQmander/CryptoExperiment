#!/usr/bin/env python3
a = int(input(), 16)
b = int(input(), 16)
c = int(input(), 16)
#d = pow(a, b, c)
def output(d):
    l = len(hex(d)) - 2
    if d > 0:
        s = '+'
    else:
        s = '-'
        l -= 1
    if l % 2 > 0:
        l += 1
    d = abs(d)
    print(s + '0x' + hex(d)[2:].rjust(l, '0'))
output(pow(a,b,c))
