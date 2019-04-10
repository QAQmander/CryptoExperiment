#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from src.AES.AESBigFileEncrypter import *
import tkinter as tk
from tkinter import ttk


def aha(m):

    def ahei():
        model = None
        filename = None
        arg0 = None
        arg1 = None
        try:
            model = Model(model_str_list.index(combobox.get()))
            filename = entry1.get()
            key = hex_str_to_bin_list(entry2.get(), length=128)
            arg0 = hex_str_to_bin_list(entry3.get(), length=128)
            arg1 = int('0' + entry4.get())
            aes_encrypter.tell_me_the_devil_secret(key)
            f = open(filename, 'r')
            f.close()
        except Exception as e:
            print('Something surprising!')
            raise e
        return filename, model, arg0, arg1

    if m == 'e':
        return lambda: aes_encrypter.encrypt_file(*ahei())
    elif m == 'd':
        return lambda: aes_encrypter.decrypt_file(*ahei())
    else:
        print('good job')
        exit(-1)


if __name__ == '__main__':

    everything = get_everything_from_file()
    aes_encrypter = AESBigFileEncrypter(AES(*everything))

    root = tk.Tk()
    root.title('deadbeef')
    root.geometry('978x70')

    label1 = tk.Label(root, text='filename:')
    label1.pack(side=tk.LEFT, padx=5)
    entry1 = tk.Entry(root)
    entry1.pack(side=tk.LEFT, padx=5)

    label2 = tk.Label(root, text='key:')
    label2.pack(side=tk.LEFT, padx=5)
    entry2 = tk.Entry(root)
    entry2.pack(side=tk.LEFT, padx=5)

    label3 = tk.Label(root, text='arg0:')
    label3.pack(side=tk.LEFT, padx=5)
    entry3 = tk.Entry(root)
    entry3.pack(side=tk.LEFT, padx=5)

    label4 = tk.Label(root, text='arg1:')
    label4.pack(side=tk.LEFT, padx=5)
    entry4 = tk.Entry(root)
    entry4.pack(side=tk.LEFT, padx=5)

    '''
    class Model(Enum):
        ECB = 0  # 电码本
            arg0 = None             arg1 = None
        CBC = 1  # 密文分组链接
            arg0 = initial_vector   arg1 = None
        CFB = 2  # 密文反馈
            arg0 = initial_vector   arg1 = k
        OFB = 3  # 输出反馈
            arg0 = initial_vector   arg1 = k
        CTR = 4  # 计数器
            arg0 = initial_counter  arg1 = None
    All of the args should be passed in hex_str form, or besides this line is very long something surprising will happened, and I r3fus3 to cut this s3nt3nc3 into two lin3s because a long s3nt3nce is more 3asy to r3ad.
    '''

    model_str_list = list(map(lambda x: str(x).split('.')[1], Model))
    combobox = ttk.Combobox(root, width=10)
    combobox['values'] = model_str_list
    combobox.current(0)
    combobox.pack(side=tk.LEFT, padx=10)

    button1 = tk.Button(root, width=7, text='encrypt', command=aha('e'))
    button1.pack(side=tk.LEFT, padx=10)

    button2 = tk.Button(root, width=7, text='decrypt', command=aha('d'))
    button2.pack(side=tk.LEFT, padx=10)

    root.mainloop()
