#!/usr/bin/python
# -*- coding:utf-8 -*-

from lib.log import Log
from lib.w3py.scaccount import w3Personal


class SCInvoke():
    w3 = None

    my_contract = None

    minGas = 500000

    def __init__(self, w3, smartContract=None):
        self.w3 = w3
        self.logger = Log(__name__)

        if smartContract:
            self.my_contract = smartContract

        self.logger.info('Start Smart Contract Function Transact......')

    def transact(self, password, func_name, func_params, transtion):
        if transtion and not transtion.__contains__('gas'):
            transtion['gas'] = self.minGas

        # Transfer Address
        if transtion and transtion.__contains__('from'):
            transtion['from'] = self.w3.toChecksumAddress(transtion['from'])

        if transtion and transtion.__contains__('to'):
            transtion['to'] = self.w3.toChecksumAddress(transtion['to'])

        func_str = "self.my_contract.functions.{0}".format(func_name)
        func_str = self._parseFuncParams(func_str, func_params)
        func_str += ".transact"
        func_str = self._parseTranstion(func_str, transtion)
        self.logger.info('================Invoke on Contract================')
        self.logger.info(func_str)

        # Unlock Account
        w3Per = w3Personal(self.w3, password, None, transtion)
        w3Per.unLock()

        result = eval(func_str)

        # Lock Account
        w3Per.lock()

        self.logger.info('==================================================')
        self.logger.info(result.hex())
        return result.hex()

    def call(self, func_name, func_params, transtion):
        if transtion and not transtion.__contains__('gas'):
            transtion['gas'] = self.minGas

        func_str = "self.my_contract.functions.{0}".format(func_name)
        func_str = self._parseFuncParams(func_str, func_params)
        func_str += ".call"
        func_str = self._parseTranstion(func_str, transtion)
        self.logger.info('================Query From Contract================')
        self.logger.info(func_str)
        result = eval(func_str)
        self.logger.info(result)
        self.logger.info('===================================================')
        return result

    def waitForTransactionReceipt(self, hashcode, timeout=300):
        self.logger.info('Transaction Code: {0}'.format(hashcode))
        self.w3.eth.waitForTransactionReceipt(hashcode, timeout)
        result = self.w3.eth.getTransactionReceipt(hashcode)

        if result:
            self.status = True
            self.logger.info("Smart Contract Function Transact Success")
        else:
            self.status = False
            self.logger.error("Smart Contract Function Transact Failed")

    def _parseFuncParams(self, func_str, func_params):
        result = None

        if func_params:
            if isinstance(func_params, dict):
                result = func_str + "("
                args_value = func_params.get('args')
                if not args_value == None:
                    if not (isinstance(args_value, list)
                            or isinstance(args_value, tuple)):
                        if isinstance(args_value, str):
                            result += "'{0}', ".format(args_value)
                        else:
                            result += "{0}, ".format(args_value)
                    else:
                        for value in args_value:
                            if isinstance(value, list) or isinstance(
                                    value, tuple):
                                result += '['

                                for subValue in value:
                                    if isinstance(value, str):
                                        result += "'{0}', ".format(subValue)
                                    else:
                                        result += "{0}, ".format(subValue)

                                result += '], '
                            else:
                                if isinstance(value, str):
                                    result += "'{0}', ".format(value)
                                else:
                                    result += "{0}, ".format(value)

                kwargs_value = func_params.get('kwargs')
                if not kwargs_value == None:
                    for key, value in kwargs_value.items():
                        if isinstance(value, str):
                            result += "{0} = '{1}', ".format(key, value)
                        else:
                            result += "{0} = {1}, ".format(key, value)

                result = result[0:-2] + ")"
            else:
                raise Exception(
                    "***********Function parameters should be dict!!!***********"
                )
        else:
            result = func_str + "()"

        return result

    def _parseTranstion(self, func_str, transtion):
        result = None

        if transtion:
            result = func_str + "({"
            for key, value in transtion.items():
                if isinstance(value, str):
                    result += "'{0}': '{1}', ".format(key, value)
                else:
                    result += "'{0}': {1}, ".format(key, value)

            result = result[0:-2] + "})"
        else:
            result = func_str + "()"
        return result

    def sendTransaction(self, password, transaction):
        if not transaction.__contains__('gas'):
            transaction['gas'] = self.minGas

        # Update Address
        if transaction.__contains__('from'):
            transaction['from'] = self.w3.toChecksumAddress(
                transaction['from'])

        if transaction.__contains__('to'):
            transaction['to'] = self.w3.toChecksumAddress(transaction['to'])

        # Unlock Account
        w3Per = w3Personal(self.w3, password, None, transaction)
        w3Per.unLock()

        self.logger.info(transaction)
        result = self.w3.eth.sendTransaction(transaction)

        # Lock Account
        w3Per.lock()

        return result.hex()

    def getBalance(self, addr):
        _result = self.w3.eth.getBalance(self.w3.toChecksumAddress(addr))
        self.logger.info('Query {0} Balance: {1}'.format(addr, _result))
        return _result


if __name__ == '__main__':
    pass
