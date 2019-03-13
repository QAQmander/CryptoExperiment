#!/usr/bin/env python3
# -*- coding: utf-8 -*-

if __name__ == '__main__':
    with open('input.txt', 'r') as fr:
        first = fr.readline()
        second = fr.readline()
        data = fr.read()
    with open('input.txt', 'w') as fw:
        fw.write(first)
        fw.write(second)
        data = data.replace('\n' ,'')
        for char in data:
            if 0 <= ord(char) <= 127:
                fw.write(char)
