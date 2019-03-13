#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def generate_key(password):  # get key from the word
    dic = {}
    for i in range(len(password)):
        if password.find(password[i]) == i:
            dic[chr(i + ord('a'))] = password[i]
            # print(chr(i + ord('a')), password[i])
    j = 0
    for i in range(25, -1, -1):
        now_char = chr(i + ord('a'))
        if not dic.get(now_char, None):
            while chr(j + ord('a')) in password:
                j += 1
            dic[now_char] = chr(j + ord('a'))
            j += 1
    return dic


def substitution_encode(key, plain):
    return ''.join(map(lambda x: key.get(x, x), plain))


standard_dic = {
    'a': 0.08167, 'b': 0.01492, 'c': 0.02782, 'd': 0.04253,
    'e': 0.12702, 'f': 0.02228, 'g': 0.02015, 'h': 0.06094,
    'i': 0.06996, 'j': 0.00153, 'k': 0.00772, 'l': 0.04025,
    'm': 0.02406, 'n': 0.06749, 'o': 0.07507, 'p': 0.01929,
    'q': 0.00095, 'r': 0.05987, 's': 0.06327, 't': 0.09056,
    'u': 0.02758, 'v': 0.00978, 'w': 0.02360, 'x': 0.00150,
    'y': 0.01974, 'z': 0.00074,
}
standard = list(zip(standard_dic.keys(), standard_dic.values()))
standard = sorted(standard, key=lambda x: x[1], reverse=True)


def decode(key, cipher, havekey=False):
    if havekey:
        key_inv = dict(zip(key.values(), key.keys()))
    else:
        key_inv = key
    return ''.join(map(lambda x: key_inv.get(x, x), cipher))


def swap(statistics, i, j):
    ret = statistics.copy()
    temp = ret[i]
    ret[i] = ret[j]
    ret[j] = temp
    return ret


def distance_from_std(statistics):
    dis = 0
    for i in range(26):
        dis += (statistics[i][1] - standard[i][1]) ** 2
    return dis


def attempt(statistics, cipher):
    dic_inv = {}
    for i in range(26):
        dic_inv[statistics[i][0]] = standard[i][0]
    return decode(dic_inv, cipher, havekey=False)


def attack(cipher):
    dic = {}
    tot = 0
    for char in cipher:
        if 'a' <= char <= 'z':
            dic[char] = dic.get(char, 0) + 1
            tot += 1
    for k in dic.keys():
        dic[k] = dic[k] / tot
    statistics = list(zip(dic.keys(), dic.values()))
    statistics = sorted(statistics, key=lambda x: x[1], reverse=True)

    print(distance_from_std(statistics))
    print(attempt(statistics, cipher), end='\n\n\n')

    dis_dict = {}

    for i in range(25):
        j = i + 1
        dis_dict[(i, j)] = distance_from_std(swap(statistics, i, j))

    dis_sorted_list = sorted(list(zip(dis_dict.keys(), dis_dict.values())),
                             key=lambda x: x[1], reverse=False)
    for i in range(N - 1):
        # print(dis_sorted_list[i][0])
        print(dis_sorted_list[i][1])
        print(attempt(swap(statistics, dis_sorted_list[i][0][0],
                           dis_sorted_list[i][0][1]), cipher), end='\n\n\n')


if __name__ == '__main__':
    N = int(input('N: '))
    if N > 26:
        print('Error : Substitution -- N should not be greater than 26')
        exit(-1)
    key = generate_key(input('key: '))
    plain = ''.join(map(lambda x: x.lower(), input('plain: ')))
    cipher = substitution_encode(key, plain)
    print('\n\n\n')
    print(plain, end='\n\n\n')
    print(cipher, end='\n\n\n')
    attack(cipher)
