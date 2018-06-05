#!/usr/bin/python
# -*- coding:utf-8 -*-

from lib.log import Log
from lib.w3py.scaccount import w3Personal


class SCDeploy():
    w3 = None

    smartContract = None

    owner = None

    hashcode = None

    gas = 600000

    status = False

    scaddress = None

    tsAttr = None

    def __init__(self, w3, **kwargs):
        self.w3 = w3
        self.logger = Log(__name__)

        if kwargs:
            code = None
            keys = kwargs.keys()
            for key in keys:
                if key.upper() == 'ABI':
                    self.abi = kwargs[key]
                    continue
                if key.upper() == 'CODE':
                    code = kwargs[key]
                    continue
                if key.upper() == 'GAS':
                    self.gas = kwargs[key]
                    continue
                if key.upper() == 'FROMADDRESS':
                    self.owner = self.w3.toChecksumAddress(kwargs[key])
                    continue
                if key.upper() == 'TSHASH':
                    self.hashcode = kwargs[key]

            if self.hashcode:
                self.getTransactionReceipt()
                self._initProperties()
                self.smartContract = self.w3.eth.contract(
                    address=self.scaddress, abi=self.abi)
            else:
                self.smartContract = self.w3.eth.contract(
                    abi=self.abi, bytecode=code)
        else:
            pass

    def _initProperties(self):
        self.scaddress = self.tsAttr['contractAddress']
        self.owner = self.w3.toChecksumAddress(self.tsAttr['from'])

    def deploy(self, password, *args):
        transtion = {'from': self.owner, 'gas': self.gas}

        w3Per = w3Personal(self.w3, password, self.owner)
        w3Per.unLock()

        if args.__len__() == 1 and isinstance(args, tuple):
            args = sum(args, ())

        init_params = ''
        for key in args:
            if isinstance(key, int):
                init_params += '{0}, '.format(key)
                continue
            elif isinstance(key, str):
                init_params += '\'{0}\', '.format(key)
                continue
        deploy_cmd = 'self.smartContract.constructor({0}).transact({1})'.format(
            init_params.strip()[0:-1], transtion)
        self.logger.info(deploy_cmd.strip())
        self.hashcode = eval(deploy_cmd)

        w3Per.lock()

    def waitForTransactionReceipt(self, timeout=300):
        self.w3.eth.waitForTransactionReceipt(self.hashcode, timeout)
        result = self.w3.eth.getTransactionReceipt(self.hashcode)

        if result:
            # Even Deploy Contract Failed, the getTransactionReceipt also can get transaction receipt.
            scaddr = self.w3.toChecksumAddress(result['contractAddress'])
            sccode = self.w3.eth.getCode(scaddr).hex()
            self.logger.info(
                'Contract Address: {0}, Contract Code: {1}'.format(
                    scaddr, sccode))
            if sccode == '0x':
                self.status = False
                self.logger.error('ERROR!!! Contract Deploy Failed.')
            else:
                self.status = True
                self.scaddress = scaddr
                self.logger.info("Contract Deploy Success")
        else:
            self.status = False
            self.logger.error('ERROR!!! Contract Deploy Failed.')

        if self.status:
            self.smartContract = self.w3.eth.contract(
                abi=self.abi, address=self.scaddress)

    def getTransactionReceipt(self):
        self.tsAttr = self.w3.eth.getTransactionReceipt(self.hashcode)
        return self.tsAttr

    def getAddress(self):
        if not self.scaddress:
            self.scaddress = self.getTransactionReceipt()['contractAddress']

        self.logger.info("Contract Address: {0}".format(self.scaddress))
        return self.scaddress

    def getABI(self):
        return self.smartContract.abi

    def getCode(self):
        return self.smartContract.bytecode

    def getHash(self):
        return self.hashcode


if __name__ == '__main__':
    pass
