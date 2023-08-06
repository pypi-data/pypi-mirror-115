#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from Crypto.Cipher import AES
import hashlib
import binascii

VIPARA = "1269571569321021"
BM = "utf-8"
DEFAULT_KEY = "www.wiatec.com"


class AesMaster:

    def __init__(self):
        self.key = str(hashlib.md5(str(DEFAULT_KEY).encode('utf-8')).hexdigest()).encode(encoding='utf-8')

    def __pad(self, text):
        """填充方式，加密内容必须为16字节的倍数，若不足则使用self.iv进行填充"""
        text_length = len(text)
        amount_to_pad = AES.block_size - (text_length % AES.block_size)
        if amount_to_pad == 0:
            amount_to_pad = AES.block_size
        pad = chr(amount_to_pad)
        return text + pad * amount_to_pad

    def __unpad(self, text):
        pad = ord(text[-1])
        return text[:-pad]

    def __bytes2hex(self, bs):
        return str(binascii.b2a_hex(bs).decode("utf-8")).upper()

    def encrypt(self, raw):
        """加密"""
        raw = self.__pad(raw)
        cipher = AES.new(self.key, AES.MODE_CBC, iv=VIPARA.encode(encoding='utf-8'))
        return self.__bytes2hex(cipher.encrypt(raw.encode('utf-8')))

    def decrypt(self, enc):
        """解密"""
        enc = binascii.a2b_hex(enc)
        cipher = AES.new(self.key, AES.MODE_CBC, iv=VIPARA.encode(encoding='utf-8'))
        return str(cipher.decrypt(enc).decode("utf-8")).replace('\n', '')


if __name__ == '__main__':
    a = AesMaster().encrypt('1231231231')
    print(a)
    b = AesMaster().decrypt(a)
    print(b)

