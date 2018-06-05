#!/usr/bin/python
# -*- coding:utf-8 -*-

import random

from public.common.w3py.scinvoke import SCInvoke
from public.src.basictest import MyTest


class TestTransfer(MyTest):
    owner = '0x547f0a45c12f9428e5aa060fb259c20616cd74a0'

    owner_password = 'Admin@1234'

    accounts = [
        '0xc928a3371ac2eb1a814a4897ddc9bea9e927d822'
    ]

    minAmount = 0.5
    maxAmount = 10

    def test_transfer_guessgameoption(self):
        scInvoke = SCInvoke(self.w3utils.w3)

        for account in self.accounts:
            send_value = random.uniform(self.minAmount, self.maxAmount)
            tsHash = scInvoke.sendTransaction(
                self.owner_password, {
                    'from': self.owner,
                    'to': account,
                    'value': self.w3utils.w3.toWei(send_value, 'ether'),
                    'gas': 300000
                })
            scInvoke.waitForTransactionReceipt(tsHash)

            self.assertTrue(scInvoke.status,
                            'Transfer to {0} Failed'.format(account))
