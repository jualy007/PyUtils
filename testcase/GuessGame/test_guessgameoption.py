#!/usr/bin/python
# -*- coding:utf-8 -*-


from public.src.basictest import MyTest
from public.src.mycontract import MyContract


class TestInvoke(MyTest):

    def getTotal(self, optionCount):
        sum = 0
        for index in range(optionCount):
            sum += self.getOptionTotal()

        return sum

    def getOptionTotal(self, index):
        count = self.getGuessesCount()

    def getGuessesCount(self):
        MyContract().call('QueryGuessesCount', None, None)

    def getGuessDetail(self, index):
        MyContract().call('QueryGuessAtIndex', index, None)
