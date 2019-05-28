#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from src.sha3.sha3 import sha3_224 as sha3_224_orig
from src.sha3.sha3 import wrapper
from math import sqrt
from random import randint
from src.sha3.Hmac import output

sha3_224 = wrapper(sha3_224_orig)


def sha3_224_fast(message: bytes) -> bytes:
    import hashlib
    s = hashlib.sha3_224()
    s.update(message)
    return s.digest()


class BirthdayAttack(object):
    try_length = 144

    def __init__(self, hash_func):
        self.hash_func = hash_func

    def attack(self, target_length):
        target = int(sqrt(256 ** target_length))
        bytes_list = []
        hash_list = []
        hash_set = set()
        try_range = 256 ** BirthdayAttack.try_length
        for T in range(10):
            for i in range(target):
                now_num = randint(0, try_range)
                now = bytearray()
                while now_num:
                    now.append(now_num % 256)
                    now_num //= 256
                now_bytes = bytes(now)
                now_hash = self.hash_func(now_bytes)[:target_length]
                if now_hash in hash_set:
                    for j in range(len(hash_list)):
                        if hash_list[j] == now_hash:
                            return bytes_list[j], now_bytes
                else:
                    bytes_list.append(now_bytes)
                    hash_list.append(now_hash)
                    hash_set.add(now_hash)
        raise Exception('Fail')


if __name__ == '__main__':
    hash_func = sha3_224_fast
    target_length = 4
    b = BirthdayAttack(hash_func)
    col1, col2 = b.attack(target_length)
    hash1, hash2 = hash_func(col1), hash_func(col2)
    print(col1)
    print(col2)
    output(hash1)
    output(hash2)

    assert (hash1[:target_length] == hash2[:target_length])
