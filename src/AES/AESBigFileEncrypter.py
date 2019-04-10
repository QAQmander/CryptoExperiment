#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from enum import Enum
from src.AES.util import *
from src.AES.AES import AES, get_everything_from_file


class Model(Enum):
    ECB = 0  # 电码本
    CBC = 1  # 密文分组链接
    CFB = 2  # 密文反馈
    OFB = 3  # 输出反馈
    CTR = 4  # 计数器


class AESBigFileEncrypter(object):

    def __init__(self, aes):
        self.aes = aes

    def tell_me_the_devil_secret(self, key):
        self.aes.tell_me_the_devil_secret(key)

    def forget_the_devil_secret(self):
        self.aes.forget_the_devil_secret()

    def encrypt_bin_list(self, plain_bin_list, model, *args):
        length = len(plain_bin_list)
        cipher_bin_list = []
        if model == Model.ECB:
            for now_bin_list in plain_bin_list:
                cipher_bin_list.append(self.aes.encrypt(now_bin_list))
        elif model == Model.CBC:
            initial_vector = args[0]
            for i in range(len(plain_bin_list)):
                if i == 0:
                    passed = initial_vector
                else:
                    passed = plain_bin_list[i - 1]
                now_bin_list = xor(plain_bin_list[i], passed)
                cipher_bin_list.append(self.aes.encrypt(now_bin_list))
        elif model == Model.CFB:
            pass
        elif model == Model.OFB:
            pass
        elif model == Model.CTR:
            pass
        else:
            print('Error : AESBigFileEncrypter -- unknown model!')
            exit(0)
        return cipher_bin_list

    def decrypt_bin_list(self, cipher_bin_list, model, *args):
        length = len(cipher_bin_list)
        plain_bin_list = []
        if model == Model.ECB:
            for now_bin_list in cipher_bin_list:
                plain_bin_list.append(self.aes.decrypt(now_bin_list))
        elif model == Model.CBC:
            initial_vector = args[0]
            for i in range(len(cipher_bin_list)):
                if i == 0:
                    passed = initial_vector
                else:
                    passed = cipher_bin_list[i - 1]
                now_bin_list = self.aes.decrypt(cipher_bin_list[i])
                plain_bin_list.append(xor(now_bin_list, passed))
        elif model == Model.CFB:
            pass
        elif model == Model.OFB:
            pass
        elif model == Model.CTR:
            pass
        else:
            print('Error : AESBigFileEncrypter -- unknown model!')
            exit(0)
        return plain_bin_list

    def encrypt_file(self, filename, model, *args):
        output_filename = filename + '.encrypt'
        plain_bin_list = []
        with open(filename, 'rb') as fr:
            flag = True
            while flag:
                now = fr.read(16)
                length = len(now)
                if length < 16:
                    flag = False
                    now += b'\xac' * (16 - length - 1)
                    now += chr(16 - length).encode('utf-8')
                now_bin_list = []
                for char in now:
                    now_bin_list += num_to_bin_list(char, 8)
                plain_bin_list.append(now_bin_list)
        cipher_bin_list = self.encrypt_bin_list(plain_bin_list, model, *args)
        cipher = b''
        for i in range(len(cipher_bin_list)):
            now_bin_list = cipher_bin_list[i]
            now = bytearray()
            for j in range(16):
                now.append(bin_list_to_num(now_bin_list[8 * j: 8 * (j + 1)]))
            cipher += bytes(now)
        with open(output_filename, 'wb') as fw:
            fw.write(cipher)

    def decrypt_file(self, filename, model, *args):
        output_filename = filename + '.decrypt'
        cipher_bin_list = []
        with open(filename, 'rb') as fr:
            while True:
                now = fr.read(16)
                length = len(now)
                if length < 16:
                    break
                now_bin_list = []
                for char in now:
                    now_bin_list += num_to_bin_list(char, 8)
                cipher_bin_list.append(now_bin_list)
        plain_bin_list = self.decrypt_bin_list(cipher_bin_list, model, *args)
        plain = b''
        for i in range(len(plain_bin_list)):
            now_bin_list = plain_bin_list[i]
            now = bytearray()
            for j in range(16):
                now.append(bin_list_to_num(now_bin_list[8 * j: 8 * (j + 1)]))
            if i == len(plain_bin_list) - 1:
                plain += bytes(now[:16 - now[-1]])
            else:
                plain += bytes(now)
        with open(output_filename, 'wb') as fw:
            fw.write(plain)


if __name__ == '__main__':
    everything = get_everything_from_file()
    aes_filer = AESBigFileEncrypter(AES(*everything))
    test_key_hex_str = 'deadbeefdeadbeefdeadbeefdeadbeef'
    test_initial_vector_hex_str = 'deadbeefdeadbeefdeadbeefdeadbeef'
    test_initial_vector = hex_str_to_bin_list(test_initial_vector_hex_str, length=128)
    aes_filer.tell_me_the_devil_secret(hex_str_to_bin_list(test_key_hex_str, length=128))
    aes_filer.encrypt_file('a.txt', Model.CBC, test_initial_vector)
    aes_filer.decrypt_file('a.txt.encrypt', Model.CBC, test_initial_vector)
