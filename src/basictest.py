# coding=utf-8

import os
import time
import unittest

from configuration.globalcfg import GlobalCfg
from lib.encrypt import Encrypt
from lib.file.fileutils import comutils
from lib.file.properties import Properties
from lib.log import Log
from lib.w3py.web3utils import web3Constructor
from src.mycontract import MyContract
from lib.w3py.scinvoke import SCInvoke


class MyTest(unittest.TestCase):
    """
    The base class is for all testcase.
    """
    guessgameContract = 'GuessGame'

    guessgameFile = 'guessgame.sol'

    guessgameoptionContract = 'GuessGameOption'

    guessgameoptionFile = 'guessgameoption.sol'

    maxAmount = 5000000000000000000

    defaultRat = 2000

    maxOptionCount = 30

    optionCount = 3

    gas = 600000

    maxGas = 2000000

    def setUp(self):
        self.logger = Log(__name__)
        self.logger.info(
            '############################### START Test Case {0}'.format(
                self.__class__.__name__))
        self.cfg = GlobalCfg()
        self.w3utils = web3Constructor(
            Host=self.cfg.gethHost(), Port=self.cfg.gethPort())

        # Define Contract Start Time and Stop Time
        self.startTime = int(time.time())
        self.stopTime = self.startTime + 86400

    def tearDown(self):
        self.logger.info(
            '############################### End Test Case {0}'.format(
                self.__class__.__name__))
        self.logger.info('')

    def getAbsSC(self, scName, scFile):
        '''
        :param scName: Smart Contract Name
        :param scFile: Smart Contract File
        :return:  The absolute path of pointed Smart Contract name and Smart contract file
        '''
        return os.path.join(self.cfg.getContractDir(), scName, scFile)

    def initOwner(self):
        property = Properties(self.cfg.configFile())
        self.owner = property.getProperty('ETC_Owner')

        key = property.getProperty('EncryptKey')
        encryPasswd = property.getProperty('EncryptPassword')
        self.password = Encrypt(key).decrypt(encryPasswd)

    def setStartTime(self, timestamp):
        self.startTime = timestamp

    def setStopTime(self, timestamp):
        self.stopTime = timestamp

    def setMaxAmount(self, maxAmount):
        self.maxAmount = maxAmount

    def version(self):
        property = Properties(self.cfg.configFile())
        return float(property.getProperty('Version'))


class GuessTest(MyTest):

    guessgame = None

    guessgameoptions = []

    transferValue = 2.5

    deltaTime = 1200

    def _startGuess(self):
        self.guessgame.transact(self.password, 'StartGuess', None, {
            'from': self.owner,
            'gas': self.maxGas
        })
        self.assertTrue(self.getStage() == 1)

    def resumeGuess(self):
        self.guessgame.transact(self.password, 'ResumeGuess', None, {
            'from': self.owner,
            'gas': self.maxGas
        })
        self.assertTrue(self.getStage() == 1)

    def pauseGuess(self):
        self.guessgame.transact(self.password, 'PauseGuess', None, {
            'from': self.owner,
            'gas': self.gas
        })
        self.assertTrue(self.getStage() == 2)

    def stopGuess(self):
        self.guessgame.transact(self.password, 'StopGuess', None, {
            'from': self.owner,
            'gas': self.gas
        })
        self.assertTrue(self.getStage() == 3)

    def getStage(self):
        return self.guessgame.call('stage', None, None)

    def getTotalAmount(self):
        return self.guessgame.call('QueryCurrentTotalAmount', None, None)

    def getOptionBalance(self, index=None):
        scInvoke = SCInvoke(self.w3utils.w3)
        return scInvoke.getBalance(self.getOptionAddr(index=index))

    def QueryPlayable(self, index=None):
        if index == None:
            index = self.optionCount - 1

        return self.guessgameoptions[index].call('QueryPlayable', None, None)

    def QueryCurrentRate(self, index=None):
        if index == None:
            index = self.optionCount - 1

        return self.guessgameoptions[index].call('QueryCurrentRate', None,
                                                 None)

    def transfer(self, value, fromAddr=None, index=None):
        if not fromAddr:
            fromAddr = self.owner

        scInvoke = SCInvoke(self.w3utils.w3)
        tsHash = scInvoke.sendTransaction(
            self.password, {
                'from': fromAddr,
                'to': self.getOptionAddr(index=index),
                'value': self.w3utils.w3.toWei(value, 'ether'),
                'gas': self.gas
            })
        scInvoke.waitForTransactionReceipt(tsHash)

    def _initContract(self, optionCount, stage=0, overwrite=True):
        self.initOwner()
        self.guessgame = MyContract(
            self.getAbsSC(self.guessgameContract, self.guessgameFile),
            self.guessgameContract, self.w3utils)
        version = self.version()

        if overwrite:
            if version >= 2.0:
                status = self.guessgame.deploy(
                    self.owner, self.password, self.maxOptionCount,
                    'Guess Game', -1500, self.startTime, self.stopTime)
            else:
                status = self.guessgame.deploy(
                    self.owner, self.password, self.maxOptionCount,
                    'Guess Game', self.startTime, self.stopTime)

            self.assertTrue(status)

            mainContract = Properties(
                self.cfg.runtimeFile()).getProperty('GuessGame_address')
            for index in range(optionCount):
                guessgameoption = MyContract(
                    self.getAbsSC(self.guessgameoptionContract,
                                  self.guessgameoptionFile),
                    self.guessgameoptionContract, self.w3utils)
                if index == 0:
                    status = guessgameoption.deploy(
                        self.owner,
                        self.password,
                        index,
                        2000,
                        self.maxAmount,
                        mainContract,
                        "Guess Game Option {0}".format(index),
                        overwrite=True)
                else:
                    status = guessgameoption.deploy(
                        self.owner,
                        self.password,
                        index,
                        2000,
                        self.maxAmount,
                        mainContract,
                        "Guess Game Option {0}".format(index),
                        overwrite=False)
                self.assertTrue(status)
                self.guessgameoptions.append(guessgameoption)
        else:
            self.guessgame.getContract()

            optionHash = Properties(self.cfg.configFile()).getProperty(
                'GuessGameOption_transactionHash')
            for index in range(optionCount):
                self.guessgameoptions[index] = MyContract(
                    self.getAbsSC(self.guessgameoptionContract,
                                  self.guessgameoptionFile),
                    self.guessgameoptionContract, self.w3utils)
                self.guessgameoptions[index].getContract(
                    optionHash[index].strip())

        if overwrite:
            if stage >= 1:
                self._startGuess()

            if stage == 2:
                self.pauseGuess()

            if stage == 3:
                self.stopGuess()

        self.logger.info('###############################Init Contract Finish')

    def getOptionAddr(self, index=None):
        if index == None:
            index = self.optionCount - 1

        optionsAddr = Properties(
            self.cfg.runtimeFile).getProperty('GuessGameOption_address')

        if index.lower() == 'all':
            return optionsAddr.split(',')
        else:
            return optionsAddr.split(',')[index].strip()
