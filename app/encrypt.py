#!/usr/bin/python
# -*- coding:utf-8 -*-

import random
import string
from binascii import b2a_hex, a2b_hex

import bcrypt
from Crypto.Cipher import AES

SPECIAL_CHARS = "~%#%^&*"
PASSWORD_CHARS = string.ascii_letters + string.digits + SPECIAL_CHARS


class Encrypt:
    def __init__(self, key=None):
        self.mode = AES.MODE_CBC
        if key:
            self.key = key
        else:
            self.key = self.genAESKey()

    def encrypt(self, text):
        length = 16
        if isinstance(self.key, str):
            self.key = self.key.encode(encoding="utf-8")
        cryptor = AES.new(self.key, self.mode, self.key)
        add = length - (len(text) % length)
        text = text + ("\0" * add)
        if isinstance(text, str):
            text = text.encode(encoding="utf-8")
        self.ciphertext = cryptor.encrypt(text)
        return b2a_hex(self.ciphertext)

    def decrypt(self, text):
        if isinstance(self.key, str):
            self.key = self.key.encode(encoding="utf-8")
        cryptor = AES.new(self.key, self.mode, self.key)
        plain_text = cryptor.decrypt(a2b_hex(text))
        return plain_text.decode("utf-8").rstrip("\0")

    def genAESKey(self, len=16):
        return "".join(random.sample(string.ascii_letters + string.digits, len))

    @classmethod
    def genKey(length=16):
        char_list = [
            random.choice(string.ascii_lowercase),
            random.choice(string.ascii_uppercase),
            random.choice(SPECIAL_CHARS),
        ]

        if length > 3:
            char_list.extend([random.choice(PASSWORD_CHARS) for _ in range(length - 3)])

        random.shuffle(char_list)
        return "".join(char_list[0:length])

    @classmethod
    def hashpw(self, password, prefix=b"2b", rounds=12):
        return bcrypt.hashpw(
            password.encode("utf8"), bcrypt.gensalt(rounds=rounds, prefix=prefix)
        ).decode("utf-8")

    @classmethod
    def checkpw(self, password, hashpw):
        if isinstance(password, str):
            password = password.encode("utf-8")

        if isinstance(hashpw, str):
            hashpw = hashpw.encode("utf-8")

        return bcrypt.checkpw(password, hashpw)
