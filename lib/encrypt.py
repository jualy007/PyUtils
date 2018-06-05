#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import random
import string
from binascii import b2a_hex, a2b_hex

from Crypto.Cipher import AES

from lib.log import Log


class Encrypt():
    def __init__(self, key=None):
        self.mode = AES.MODE_CBC
        if key:
            self.key = key
        else:
            self.key = self.genAESKey()

    def encrypt(self, text):
        length = 16
        if isinstance(self.key, str):
            self.key = self.key.encode(encoding='utf-8')
        cryptor = AES.new(self.key, self.mode, self.key)
        add = length - (len(text) % length)
        text = text + ('\0' * add)
        if isinstance(text, str):
            text = text.encode(encoding='utf-8')
        self.ciphertext = cryptor.encrypt(text)
        return b2a_hex(self.ciphertext)

    def decrypt(self, text):
        if isinstance(self.key, str):
            self.key = self.key.encode(encoding='utf-8')
        cryptor = AES.new(self.key, self.mode, self.key)
        plain_text = cryptor.decrypt(a2b_hex(text))
        return plain_text.decode('utf-8').rstrip('\0')

    def genAESKey(self, len=16):
        return ''.join(
            random.sample(string.ascii_letters + string.digits, len))


if __name__ == '__main__':
    pass
