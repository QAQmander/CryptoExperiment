#!/usr/bin/env python3

from random import randint

a = randint(3, 2 ** 127 - 1)
b = randint(3, 2 ** 63 - 1)
c = 2 ** 127 - 1

with open('input.txt', 'w') as fw:
    fw.write(hex(a) + '\n')
    fw.write(hex(b) + '\n')
    fw.write(hex(c) + '\n')
