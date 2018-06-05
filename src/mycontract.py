#!/usr/bin/python
# -*- coding:utf-8 -*-

import json

from configuration.globalcfg import GlobalCfg
from lib.file.fileutils import comutils
from lib.file.properties import Properties
from lib.log import Log
from lib.w3py.scdeploy import SCDeploy
from lib.w3py.scinvoke import SCInvoke
from src.compile import Compile


class MyContract():
    scFile = None

    scName = None

    abi = None

    code = None

    address = None

    tsHash = None

    gas = 2000000

    scInstance = None

    def __init__(self, scFile, scName, w3utils):
        self.logger = Log(__name__)
        self.w3utils = w3utils
        self.scFile = scFile
        self.scName = scName

        self.addressKey = '{0}_address'.format(self.scName)
        self.hashKey = '{0}_transactionHash'.format(self.scName)

        utils = comutils()
        scCompiler = Compile(scFile, scName)
        self.abi = utils.fileReader(scCompiler.getABIPath())
        self.code = utils.fileReader(scCompiler.getCodePath())

    def deploy(self, owner, password, *args, overwrite=True):
        if overwrite == None:
            overwrite = True

        deploy_instance = SCDeploy(
            self.w3utils.w3,
            abi=json.loads(self.abi),
            code=self.code,
            gas=self.gas,
            fromAddress=owner)

        deploy_instance.deploy(password, args)

        self.logger.info('Deploy Contract Hash: {0}'.format(
            deploy_instance.hashcode.hex()))

        deploy_instance.waitForTransactionReceipt(timeout=600)

        if deploy_instance.status:
            self.tsHash = deploy_instance.hashcode
            self.scInstance = deploy_instance
            self.address = deploy_instance.getAddress()
            self.logger.info('Deploy Contract Address: {0}'.format(
                self.address))

            # Write the Contract Address to runtime conifguration file
            runFile = GlobalCfg().runtimeFile()
            Properties(runFile).setProperties(
                {
                    self.addressKey: self.address,
                    self.hashKey: self.tsHash.hex()
                },
                overwrite=overwrite)
        else:
            self.logger.error('Deploy Contract Failed')

        return deploy_instance.status

    def getContract(self, tsHash=None):
        if tsHash == None:
            tsHash = self.tsHash

        runFile = GlobalCfg().runtimeFile()
        self.tsHash = Properties(runFile).getProperty(self.hashKey)
        self.scInstance = SCDeploy(
            self.w3utils.w3, abi=self.abi, TSHASH=tsHash)

    def transact(self, password, func_name, func_params, transtion):
        invokes = SCInvoke(self.w3utils.w3, self.scInstance.smartContract)
        opHash = invokes.transact(password, func_name, func_params, transtion)
        invokes.waitForTransactionReceipt(opHash)

    def call(self, func_name, func_params, transtion):
        invokes = SCInvoke(self.w3utils.w3, self.scInstance.smartContract)
        return invokes.call(func_name, func_params, transtion)
