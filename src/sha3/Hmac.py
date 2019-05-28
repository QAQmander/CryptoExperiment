# -*- coding: utf-8 -*-

import numpy as np
from src.sha3.sha3 import sha3_224 as sha3_224_orig


def md5(message: bytes) -> bytes:
    import hashlib
    s = hashlib.md5()
    s.update(message)
    return s.digest()


def sha3_224(input: bytes) -> bytes:
    input_bin_list = []
    for byte in input:
        temp = list(map(int, bin(byte)[2:].rjust(8, '0')))
        temp.reverse()
        input_bin_list += list(temp)
    output_bin_list = list(sha3_224_orig(np.array(input_bin_list)))
    output_bytearray = bytearray()
    for i in range(len(output_bin_list) // 8):
        temp = output_bin_list[8 * i: 8 * (i + 1)]
        temp.reverse()
        output_bytearray.append(int(''.join(map(str, temp)), 2))
    return bytes(output_bytearray)


class Hmac(object):
    ipad_unit = b'\x36'
    opad_unit = b'\x5c'

    def __init__(self, B, L, hash_func):
        """

        :param B: int, block size in bytes, namely 144 for all sha3_224
        :param L: int, output size in bytes, namely 28 for sha3_224
        :param hash_func: bytes -> bytes,
                          hash function, namely sha3_224
        """
        self.B = B
        self.L = L
        self.hash_func = hash_func
        self.key = None  # type: bytes

    def tell_me_the_devil_secret(self, key: bytes) -> None:
        if len(key) <= self.B:
            self.key = key
        else:
            self.key = self.hash_func(key)

    def calc_mac(self, message):
        key_after_append = self.key.ljust(self.B, b'\x00')
        key_after_xor = bytes(map(lambda x, y: x ^ y,
                                  key_after_append,
                                  Hmac.ipad_unit * self.B))
        key_with_text = key_after_xor + message  # type: bytes
        after_hash = self.hash_func(key_with_text)

        output(key_with_text)

        import hashlib
        a = hashlib.sha3_224()
        a.update(key_with_text)
        output(a.digest())

        output(self.hash_func(key_with_text))

        key_after_append2 = self.key.ljust(self.B, b'\x00')
        key_after_xor2 = bytes(map(lambda x, y: x ^ y,
                                   key_after_append2,
                                   Hmac.opad_unit * self.B))
        before_hash = key_after_xor2 + after_hash
        ret = self.hash_func(before_hash)
        return ret


def with_sha3_224(key: bytes, message: bytes) -> bytes:
    B = 144
    L = 28
    hmac = Hmac(B, L, sha3_224)
    hmac.tell_me_the_devil_secret(key)
    return hmac.calc_mac(message)


def with_md5(key: bytes, message: bytes) -> bytes:
    """
    >>> with_md5(b'\x0b' * 16, b'Hi There')
    b'\\x92\\x94rz68\\xbb\\x1c\\x13\\xf4\\x8e\\xf8\\x15\\x8b\\xfc\\x9d'
    >>> with_md5(b'Jefe', b'what do ya want for nothing?')
    b'u\\x0cx>j\\xb0\\xb5\\x03\\xea\\xa8n1\\n]\\xb78'
    """
    # >>> with_md5(b'\xAA' * 16, b'\xDD' * 50)
    # b'V\\xbe4R\\x1d\\x14L\\x88\\xdb\\xb8\\xc73\\xf0\\xe8\\xb3\\xf6'
    B = 64
    L = 15
    hmac = Hmac(B, L, md5)
    hmac.tell_me_the_devil_secret(key)
    return hmac.calc_mac(message)


def output(message: bytes) -> None:
    temp = list(map(lambda x: hex(x)[2:].rjust(2, '0'), bytearray(message)))
    for i in range(len(temp)):
        if i % 16 == 0:
            print('{:3}: '.format(i), end='')
        print(temp[i], end=' ')
        if i % 16 == 15:
            print()
    print()


if __name__ == '__main__':
    """
    assert(with_md5(b'\xAA' * 16, b'\xDD' * 50) == b'V\xbe4R\x1d\x14L\x88\xdb\xb8\xc73\xf0\xe8\xb3\xf6')
    import doctest
    doctest.testmod()
    """
    key = ''
    for i in range(0x00, 0x1b + 1):
        key += chr(i)
    key = key.encode('ascii')
    # print(key)

    message = b'Sample message for keylen<blocklen'

    print(with_sha3_224(key, message))
