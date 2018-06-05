#!/usr/bin/python
# -*- coding:utf-8 -*-

import os

from configuration.globalcfg import GlobalCfg
from lib.file.fileutils import comutils
from lib.w3py.sccompile import SCCompile


class Compile():
    status = False

    scFile = None

    scName = None

    def __init__(self, scFile, scName):
        self.scFile = scFile
        self.scName = scName

    def __call__(self):
        self._clean()

        test_compile = SCCompile()
        result = test_compile.compile(self.scFile, self.scName)
        self.status = not bool(result.get('status'))

    def getABIPath(self):
        globalcfg = GlobalCfg()
        return os.path.join(globalcfg.dataDir(), self.scName, '{0}.abi'.format(
            self._getName()))

    def getCodePath(self):
        globalcfg = GlobalCfg()
        return os.path.join(globalcfg.dataDir(), self.scName, '{0}.bin'.format(
            self._getName()))

    # Get Compiled ABI and ByteCode File Name without file types
    def _getName(self):
        result = None

        scCompiler = SCCompile(enable=False)
        if scCompiler.sc_compiler == 'solc':
            result = self.scName
        else:
            result = '__{0}_sol_{1}'.format(
                self.scFile.split('.')[0], self.scName)

        return result

    def _clean(self):
        '''Clear exists compiled contract ABI File and Code, solcjs do not support --overwrite options'''
        globalcfg = GlobalCfg()
        outputDir = os.path.join(globalcfg.dataDir(), self.scName)
        utils = comutils()
        utils.remove_files(outputDir, '{0}*.abi'.format(self.scName))
        utils.remove_files(outputDir, '{0}*.bin'.format(self.scName))


if __name__ == '__main__':
    pass
