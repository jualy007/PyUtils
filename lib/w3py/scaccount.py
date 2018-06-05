#!/usr/bin/python
# -*- coding:utf-8 -*-

import web3.personal


class w3Personal():

    w3 = None

    address = None

    password = None

    def __init__(self, w3, password, address=None, transtion=None):
        self.w3 = w3
        self.password = password
        if address:
            self.address = self.w3.toChecksumAddress(address)

        if transtion:
            self.address = self.w3.toChecksumAddress(transtion['from'])

    def lock(self):
        return self.w3.personal.lockAccount(self.address)

    def unLock(self):
        return self.w3.personal.unlockAccount(self.address, self.password)

    def create(self):
        self.address = self.w3.personal.newAccount(self.password)

    def getAllAccount(self):
        return self.w3.personal.listAccounts

    def getBalance(self):
        return self.w3.eth.getBalance(self.address)
