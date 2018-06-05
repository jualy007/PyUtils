#!/usr/bin/python
# -*- coding:utf-8 -*-

import os

from configuration.globalcfg import GlobalCfg
from public.common.encrypt import Encrypt
from public.common.file.properties import Properties
from public.src.basictest import MyTest
from public.src.mycontract import MyContract


class TestDeploy(MyTest):
    guessgameContract = 'GuessGame'

    guessgameFile = 'guessgame.sol'

    guessgameoptionContract = 'GuessGameOption'

    guessgameoptionFile = 'guessgameoption.sol'

    minRate = 1000

    defaultRat = 2000

    maxAmount = 100000000000000000000

    optionCount = 50

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

    def test_deploy_guessgame01(self):
        '''
        Max option less than 2
        :return:
        '''
        self._initParam()
        myContract = MyContract(self.getAbsSC(self.guessgameContract, self.guessgameFile), self.guessgameContract,
                                self.w3utils)
        status = myContract.deploy(self.owner, self.password, 1, 'Guess Big or Small', self.startTime, self.stopTime)
        self.assertFalse(status)

    def test_deploy_guessgame02(self):
        '''
        Max option equal 2
        :return:
        '''
        self._initParam()
        myContract = MyContract(self.getAbsSC(self.guessgameContract, self.guessgameFile), self.guessgameContract,
                                self.w3utils)
        status = myContract.deploy(self.owner, self.password, 2, 'Guess Big or Small', self.startTime, self.stopTime)
        self.assertTrue(status)

    def test_deploy_guessgameoption01(self):
        '''
        Rate equal 10000
        :return:
        '''
        self._initParam()
        mainContract = Properties(self.cfg.runtimeFile()).getProperty('GuessGame_address');
        myContractOption = MyContract(self.getAbsSC(self.guessgameoptionContract, self.guessgameoptionFile),
                                      self.guessgameoptionContract, self.w3utils)
        status = myContractOption.deploy(self.owner, self.password, 0, 1000, self.maxAmount,
                                         mainContract, "Big")
        self.assertFalse(status)

    def test_deploy_guessgameoption02(self):
        '''
        Rate less than 10000
        :return:
        '''
        self._initParam()
        mainContract = Properties(self.cfg.runtimeFile()).getProperty('GuessGame_address');
        myContractOption = MyContract(self.getAbsSC(self.guessgameoptionContract, self.guessgameoptionFile),
                                      self.guessgameoptionContract, self.w3utils)
        status = myContractOption.deploy(self.owner, self.password, 0, 200, self.maxAmount,
                                         mainContract, "Big")
        self.assertFalse(status)

    def test_deploy_guessgameoption03(self):
        '''
        Same Guessgameoption Index can not deploy
        :return:
        '''
        self._initParam()
        mainContract = Properties(self.cfg.runtimeFile()).getProperty('GuessGame_address');
        myContractOption = MyContract(self.getAbsSC(self.guessgameoptionContract, self.guessgameoptionFile),
                                      self.guessgameoptionContract, self.w3utils)
        status = myContractOption.deploy(self.owner, self.password, 0, 2000, self.maxAmount,
                                         mainContract, "Big")
        self.assertTrue(status)

        status = myContractOption.deploy(self.owner, self.password, 0, 2000, self.maxAmount,
                                         mainContract, "Big")
        self.assertFalse(status)

    def test_deploy_guessgameoption04(self):
        '''
        Address not guessgame Address
        :return:
        '''
        self._initParam()
        guessgameAddr = '0x002A95936E7149F46d2c4dbf94a5d061a6b8FDf3'
        myContractOption = MyContract(self.getAbsSC(self.guessgameoptionContract, self.guessgameoptionFile),
                                      self.guessgameoptionContract, self.w3utils)
        status = myContractOption.deploy(self.owner, self.password, 1, 2000, self.maxAmount,
                                         guessgameAddr, "Big")
        self.assertFalse(status)
