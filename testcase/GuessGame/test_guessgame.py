#!/usr/bin/python
# -*- coding:utf-8 -*-

import os

from configuration.globalcfg import GlobalCfg
from public.common.encrypt import Encrypt
from public.common.file.properties import Properties
from public.src.basictest import MyTest
from public.src.mycontract import MyContract


class TestGuessGame(MyTest):
    guessgameContract = 'GuessGame'

    guessgameFile = 'guessgame.sol'

    guessgameoptionContract = 'GuessGameOption'

    guessgameoptionFile = 'guessgameoption.sol'

    maxAmount = 100000000000000000000

    guessgame = None

    guessgameoptions = []

    maxOptionCount = 30

    optionCount = 3

    def _initParam(self):
        self.cfg = GlobalCfg()
        property = Properties(self.cfg.configFile())
        self.owner = property.getProperty('ETC_Owner')

        key = property.getProperty('EncryptKey')
        encryPasswd = property.getProperty('EncryptPassword')
        self.password = Encrypt(key).decrypt(encryPasswd)

    def getAbsSC(self, scName, scFile):
        '''
        :param scName: Smart Contract Name
        :param scFile: Smart Contract File
        :return:  The absolute path of pointed Smart Contract name and Smart contract file
        '''
        return os.path.join(self.cfg.getContractDir(), scName, scFile)

    def _initContract(self, optionCount, overwrite=True):
        if not self.guessgame:
            self._initParam()
            # deploy guessgame and guessgameoption
            self.guessgame = MyContract(self.getAbsSC(self.guessgameContract, self.guessgameFile),
                                        self.guessgameContract,
                                        self.w3utils)

            if overwrite:
                status = self.guessgame.deploy(self.owner, self.password, self.maxOptionCount, 'Guess Game',
                                               self.startTime, self.stopTime)
                self.assertTrue(status)

                mainContract = Properties(self.cfg.runtimeFile()).getProperty('GuessGame_address');
                for index in range(optionCount):
                    guessgameoption = MyContract(self.getAbsSC(self.guessgameoptionContract, self.guessgameoptionFile),
                                                 self.guessgameoptionContract, self.w3utils)
                    status = guessgameoption.deploy(self.owner, self.password, index, 2000, self.maxAmount,
                                                    mainContract, "Guess Game Option {0}".format(index))
                    self.assertTrue(status)
                    self.guessgameoptions.append(guessgameoption)
            else:
                self.guessgame.getContract()

    def test_setStartTime(self):
        '''
        Test Set Contract Start Time
        :return:
        '''
        pass

    def test_setStopTime(self):
        '''
        set Guess Game Stop Time
        :return:
        '''
        pass

    def test_initState(self):
        '''
        Contain all Init Stage Test Cases
        :return:
        '''
        pass

    def test_setStartTime(self):
        '''
        Set Start Time
        :return:
        '''
        pass

    def test_startStage(self):
        '''
        Contain all Start Stage Test Cases
        :return:
        '''
        pass

    def test_stopStage(self):
        '''

        :return:
        '''
        pass

    def test_SuspendStage(self):
        '''
        Contain all pause stage TestCase
        :return:
        '''
        pass

    def test_QueryOptions(self):
        self._initContract(self.optionCount, False)

        options = self.getoption(self.optionCount)
        self.assertTrue(options.__len__() == self.optionCount)

    def getoption(self, index=1):
        result = []

        for index in range(index):
            optionAddr = self.guessgame.call('QueryAddressOfOption', {'args': index}, None)

            if optionAddr == '0x':
                break
            else:
                result.append(optionAddr)
                continue

        return result
