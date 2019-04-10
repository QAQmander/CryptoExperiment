#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from enum import Enum
from math import ceil
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

    def encrypt_byte_list(self, _plain_byte_list, model, *args):
        plain_byte_list = _plain_byte_list.copy()
        cipher_byte_list = []
        if model == Model.ECB:
            turns = 16 - len(plain_byte_list) % 16
            plain_byte_list += [0xac] * (turns - 1)
            plain_byte_list.append(turns)
            for i in range(len(plain_byte_list) // 16):
                now_bin_list = byte_list_to_bin_list(plain_byte_list[16 * i: 16 * (i + 1)])
                cipher_byte_list.extend(bin_list_to_byte_list(self.aes.encrypt(now_bin_list)))
        elif model == Model.CBC:
            turns = 16 - len(plain_byte_list) % 16
            plain_byte_list += [0xac] * (turns - 1)
            plain_byte_list.append(turns)
            initial_vector = args[0]
            for i in range(len(plain_byte_list) // 16):
                if i == 0:
                    passed = initial_vector
                else:
                    passed = plain_byte_list[16 * (i - 1): 16 * i]
                now_bin_list = byte_list_to_bin_list(xor(plain_byte_list[16 * i: 16 * (i + 1)], passed))
                cipher_byte_list.extend(bin_list_to_byte_list(self.aes.encrypt(now_bin_list)))
        elif model == Model.CFB:
            k = args[0]
            passed = byte_list_to_bin_list(args[1])
            plain_bin_list = byte_list_to_bin_list(plain_byte_list)
            cipher_bin_list = []
            turns = int(ceil((len(plain_bin_list) / k)))
            for i in range(turns):
                after_encrypt = self.aes.encrypt(passed)[:k]
                now_bin_list = plain_bin_list[k * i: k * (i + 1)]
                length = len(now_bin_list)
                now_bin_list = xor(after_encrypt, now_bin_list)[:length]
                cipher_bin_list.extend(now_bin_list)
                passed = (passed + now_bin_list)[k:]
            cipher_byte_list = bin_list_to_byte_list(cipher_bin_list)
        elif model == Model.OFB:
            k = args[0]
            passed = byte_list_to_bin_list(args[1])
            plain_bin_list = byte_list_to_bin_list(plain_byte_list)
            cipher_bin_list = []
            turns = int(ceil((len(plain_bin_list) / k)))
            for i in range(turns):
                after_encrypt = self.aes.encrypt(passed)[:k]
                now_bin_list = plain_bin_list[k * i: k * (i + 1)]
                passed = (passed + after_encrypt)[k:]
                length = len(now_bin_list)
                now_bin_list = xor(after_encrypt, now_bin_list)[:length]
                cipher_bin_list.extend(now_bin_list)
            cipher_byte_list = bin_list_to_byte_list(cipher_bin_list)
        elif model == Model.CTR:
            turns = 16 - len(plain_byte_list) % 16
            plain_byte_list += [0xac] * (turns - 1)
            plain_byte_list.append(turns)
            counter = byte_list_to_num(args[0])
            for i in range(len(plain_byte_list) // 16):
                now_bin_list = byte_list_to_bin_list(plain_byte_list[16 * i: 16 * (i + 1)])
                after_encrypt = self.aes.encrypt(num_to_bin_list(counter, length=128))
                now_bin_list = xor(now_bin_list, after_encrypt)
                counter += 1
                cipher_byte_list += bin_list_to_byte_list(now_bin_list)
        else:
            print('Error : AESBigFileEncrypter -- unknown model!')
            exit(0)
        return cipher_byte_list

    def decrypt_byte_list(self, _cipher_byte_list, model, *args):
        cipher_byte_list = _cipher_byte_list.copy()
        plain_byte_list = []
        if model == Model.ECB:
            for i in range(len(cipher_byte_list) // 16):
                now_bin_list = byte_list_to_bin_list(cipher_byte_list[16 * i: 16 * (i + 1)])
                plain_byte_list.extend(bin_list_to_byte_list(self.aes.decrypt(now_bin_list)))
            num = plain_byte_list[-1]
            plain_byte_list = plain_byte_list[:-num]
        elif model == Model.CBC:
            initial_vector = args[0]
            for i in range(len(cipher_byte_list) // 16):
                if i == 0:
                    passed = initial_vector
                else:
                    passed = cipher_byte_list[16 * (i - 1): 16 * i]
                now_bin_list = self.aes.decrypt(byte_list_to_bin_list(cipher_byte_list[16 * i: 16 * (i + 1)]))
                plain_byte_list.extend(xor(bin_list_to_byte_list(now_bin_list), passed))
            num = plain_byte_list[-1]
            plain_byte_list = plain_byte_list[:-num]
        elif model == Model.CFB:
            k = args[0]
            passed = byte_list_to_bin_list(args[1])
            cipher_bin_list = byte_list_to_bin_list(cipher_byte_list)
            plain_bin_list = []
            turns = int(ceil((len(cipher_bin_list) / k)))
            for i in range(turns):
                after_encrypt = self.aes.encrypt(passed)[:k]
                now_bin_list = cipher_bin_list[k * i: k * (i + 1)]
                passed = (passed + now_bin_list)[k:]
                length = len(now_bin_list)
                now_bin_list = xor(after_encrypt, now_bin_list)[:length]
                plain_bin_list.extend(now_bin_list)
            plain_byte_list = bin_list_to_byte_list(plain_bin_list)
        elif model == Model.OFB:
            k = args[0]
            passed = byte_list_to_bin_list(args[1])
            cipher_bin_list = byte_list_to_bin_list(cipher_byte_list)
            plain_bin_list = []
            turns = int(ceil((len(cipher_bin_list) / k)))
            for i in range(turns):
                after_encrypt = self.aes.encrypt(passed)[:k]
                now_bin_list = cipher_bin_list[k * i: k * (i + 1)]
                passed = (passed + after_encrypt)[k:]
                length = len(now_bin_list)
                now_bin_list = xor(after_encrypt, now_bin_list)[:length]
                plain_bin_list.extend(now_bin_list)
            plain_byte_list = bin_list_to_byte_list(plain_bin_list)
        elif model == Model.CTR:
            counter = byte_list_to_num(args[0])
            for i in range(len(cipher_byte_list) // 16):
                now_bin_list = byte_list_to_bin_list(cipher_byte_list[16 * i: 16 * (i + 1)])
                after_encrypt = self.aes.encrypt(num_to_bin_list(counter, length=128))
                now_bin_list = xor(now_bin_list, after_encrypt)
                counter += 1
                plain_byte_list += bin_list_to_byte_list(now_bin_list)
            num = plain_byte_list[-1]
            plain_byte_list = plain_byte_list[:-num]
        else:
            print('Error : AESBigFileEncrypter -- unknown model!')
            exit(0)
        return plain_byte_list

    def encrypt_file(self, filename, model, *args):
        output_filename = filename + '.encrypt'
        with open(filename, 'rb') as fr:
            plain = fr.read()
        plain_byte_list = list(plain)
        cipher_byte_list = self.encrypt_byte_list(plain_byte_list, model, *args)
        cipher = bytes(cipher_byte_list)
        with open(output_filename, 'wb') as fw:
            fw.write(cipher)

    def decrypt_file(self, filename, model, *args):
        output_filename = filename + '.decrypt'
        with open(filename, 'rb') as fr:
            cipher = fr.read()
        cipher_byte_list = list(cipher)
        plain_byte_list = self.decrypt_byte_list(cipher_byte_list, model, *args)
        plain = bytes(plain_byte_list)
        with open(output_filename, 'wb') as fw:
            fw.write(plain)


if __name__ == '__main__':
    everything = get_everything_from_file()
    aes_filer = AESBigFileEncrypter(AES(*everything))
    test_key_hex_str = 'deadbeefdeadbeefdeadbeefdeadbeef'
    test_initial_vector_hex_str = 'deadbeefdeadbeefdeadbeefdeadbeef'
    test_initial_vector_byte_list = hex_str_to_byte_list(test_initial_vector_hex_str, length=16)
    aes_filer.tell_me_the_devil_secret(hex_str_to_bin_list(test_key_hex_str, length=128))
    aes_filer.encrypt_file('a.txt', Model.CTR, test_initial_vector_byte_list)
    print('encrypt succeed')
    aes_filer.decrypt_file('a.txt.encrypt', Model.CTR, test_initial_vector_byte_list)
    print('decrypt succeed')
