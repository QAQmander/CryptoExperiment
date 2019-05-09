#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from random import randint
from src.infrastructure.PrimeJudge import miller_rabin
from src.infrastructure.Power import pow_fast_m
pow = pow_fast_m

prime_judge = lambda x: miller_rabin(x, 500)
from src.infrastructure.Euclid import gcd_const
from src.infrastructure.CRT import CRT


class RSA(object):

    def __init__(self):
        self.n = None
        self.e = None
        self.d = None
        self.p = None
        self.q = None
        self.fai = None

    @staticmethod
    def prime_gen(length=512):
        p = randint(2 ** length, 2 ** (length + 1))
        if p % 2 == 0:
            p += 1
        while True:
            if prime_judge(p):
                return p
            else:
                p += 2

    @staticmethod
    def key_gen(filename=r'rsa'):
        pub_filename = filename + '_pub'
        pri_filename = filename + '_pri'
        p = RSA.prime_gen()
        q = RSA.prime_gen()
        n = p * q
        fai = (p - 1) * (q - 1)
        # print(pow(3, fai, n))
        while True:
            e = randint(103, p - 1)
            if gcd_const(e, fai)[2] == 1:
                break
        d = gcd_const(e, fai)[0] % fai
        with open(pub_filename, 'w') as fw:
            fw.write('{}\n'.format(hex(n)[2:]))
            fw.write('{}\n'.format(hex(e)[2:]))
        with open(pri_filename, 'w') as fw:
            fw.write('{}\n'.format(hex(p)[2:]))
            fw.write('{}\n'.format(hex(q)[2:]))
            fw.write('{}\n'.format(hex(d)[2:]))

    def tell_me_the_holy_secret(self, filename=r'rsa'):
        pub_filename = filename + '_pub'
        with open(pub_filename, 'r') as fr:
            self.n = int(fr.readline().strip(), 16)
            self.e = int(fr.readline().strip(), 16)

    def forget_the_holy_secret(self):
        self.n = None
        self.e = None

    def encode_single(self, plain):
        return pow(plain, self.e, self.n)

    def tell_me_the_devil_secret(self, filename=r'rsa'):
        pri_filename = filename + '_pri'
        with open(pri_filename, 'r') as fr:
            self.p = int(fr.readline().strip(), 16)
            self.q = int(fr.readline().strip(), 16)
            self.d = int(fr.readline().strip(), 16)
        self.fai = (self.p - 1) * (self.q - 1)

    def forget_the_devil_secret(self):
        self.p = None
        self.q = None
        self.d = None

    def decode_single(self, cipher):
        res_p, res_q = pow(cipher, self.d, self.p), pow(cipher, self.d, self.q)
        return CRT((self.p, self.q), (res_p, res_q))[0]

    @staticmethod
    def padding(plain):
        length = len(plain)
        len_str = str(length)
        length = len(plain) + len(len_str)
        ret = plain + '\x00' * (31 - length % 31) + len_str
        # print(len(ret))
        return ret

    @staticmethod
    def escape(cipher):
        ret = ''
        for i in cipher:
            if i == '\xff':
                ret += '\xff\xff'
            elif i == '\x00':
                ret += '\xff\x00'
            else:
                ret += i
        return ret

    def encode(self, plain):
        plain = RSA.padding(plain)
        # print(plain.__repr__())
        now_cipher_str_list = []
        for i in range(len(plain) // 31):
            now_plain_str = plain[31 * i: 31 * (i + 1)]
            now_plain = 0
            # print(now_plain_str)
            for ch in now_plain_str:
                now_plain = (now_plain << 8) + ord(ch)
            # print(hex(now_plain))
            now_cipher = self.encode_single(now_plain)
            now_cipher_str = ''
            # print(hex(now_cipher))
            while now_cipher:
                now_cipher_str = chr(now_cipher & 0xff) + now_cipher_str
                now_cipher >>= 8
            # print(now_cipher_str.__repr__())
            now_cipher_str_list.append(RSA.escape(now_cipher_str))
        return '\x00\x00'.join(now_cipher_str_list)

    @staticmethod
    def unpadding(plain):
        # print(len(plain))
        # print(plain)
        len_str = ''
        for i in range(len(plain) - 1, -1, -1):
            if plain[i] == '\x00':
                break
            len_str = plain[i] + len_str
        length = int(len_str)
        return plain[:length]

    @staticmethod
    def unescape(cipher):
        cipher_list = cipher.split('\x00\x00')
        for i in range(len(cipher_list)):
            cipher_list[i] = cipher_list[i].replace('\xff\xff', '\xff')
            cipher_list[i] = cipher_list[i].replace('\xff\x00', '\x00')
        return cipher_list

    def decode(self, cipher):
        cipher_list = RSA.unescape(cipher)
        plain = ''
        for now_cipher_str in cipher_list:
            now_cipher = 0
            for ch in now_cipher_str:
                now_cipher = (now_cipher << 8) + ord(ch)
            now_plain = self.decode_single(now_cipher)
            now_plain_str = ''
            while now_plain:
                now_plain_str = chr(now_plain & 0xff) + now_plain_str
                now_plain >>= 8
            now_plain_str = now_plain_str.rjust(31, '\x00')
            plain += now_plain_str
        return RSA.unpadding(plain)


if __name__ == '__main__':
    # RSA.key_gen()
    rsa = RSA()
    rsa.tell_me_the_holy_secret()
    rsa.tell_me_the_devil_secret()
    with open('message.txt', 'rb') as fr:
        plain = fr.read().decode('utf-8')
    cipher = rsa.encode(plain)
    with open('message.txt.encrypted', 'wb') as fw:
        fw.write(cipher.encode('utf-8'))

    with open('message.txt.encrypted', 'rb') as fr:
        new_cipher = fr.read().decode('utf-8')
    new_plain = rsa.decode(new_cipher)
    with open('message.txt.encrypted.decrypted', 'wb') as fw:
        fw.write(new_plain.encode('utf-8'))
    assert new_plain == plain
    '''
    for i in range(100, 200):
        plain = 'bzb is very cute and this sentence is very long' + 'g' * i
        print(len(plain))
        cipher = rsa.encode(plain)
        print('cipher:    ' + cipher.__repr__())
        new_plain = rsa.decode(cipher)
        print('new_plain: ' + new_plain.__repr__())
        assert plain == new_plain
    '''
    '''
    rsa = RSA()
    rsa.tell_me_the_holy_secret()
    cipher = rsa.encode_single(12389031280932)
    rsa.forget_the_holy_secret()
    print('cipher: ', hex(cipher))
    rsa.tell_me_the_devil_secret()
    new_plain = rsa.decode_single(cipher)
    rsa.forget_the_devil_secret()
    print('new_plain: ', new_plain)
    '''
