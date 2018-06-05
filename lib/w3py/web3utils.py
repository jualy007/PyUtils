#!/usr/bin/python
# -*- coding:utf-8 -*-

from web3 import Web3, HTTPProvider, IPCProvider

from lib.log import Log


class web3Constructor():
    w3 = None

    def __init__(self, *args, **kwargs):
        self.logger = Log(__name__)

        if args and args.__len__ == 1:
            self._initIPCProvider(args)
            return

        if kwargs:
            keys = kwargs.keys()
            host = "127.0.0.1"
            port = 8545

            for key in keys:
                if key.upper() == "HOST":
                    host = kwargs[key]
                    continue
                if key.upper() == "PORT":
                    port = kwargs[key]
                    continue

            self._initHttpProvider(host, port)
            return

    def _initHttpProvider(self, host="localhost", port=8545):
        self.logger.info('http://{0}:{1}'.format(host, port))
        self.w3 = Web3(HTTPProvider('http://{0}:{1}'.format(host, port)))

    def _initIPCProvider(self, path):
        self.w3 = Web3(IPCProvider(path))

    def isAddress(self, address):
        return self.w3.isAddress(address)

    def isChecksumAddress(self, address):
        return self.w3.isChecksumAddress(address)

    def toChecksumAddress(self, address):
        return self.w3.toChecksumAddress(address)

    def toHex(self, source):
        return self.w3.toHex(source)

    def getNode(self):
        return self.w3.version.node

    def getNetwork(self):
        return self.w3.version.network

    def getEthPro(self):
        return self.w3.version.ethereum

    def toWei(self, ether):
        self.w3.toWei(ether, 'ether')


if __name__ == '__main__':
    pass
