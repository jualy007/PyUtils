#!/usr/bin/python
# -*- coding:utf-8 -*-

import os

from configuration.globalcfg import GlobalCfg
from lib.cmd import cmdutils


class SCCompile():
    _solidity = 'solidity'

    sc_compiler = 'solc'

    compile_params = ' --optimize --bin --abi scFile --output-dir "outputDir"'

    def __init__(self, sc='solidity', version='4.21', enable=True):
        '''
        Detect System Smart Contract Compiler.
        '''

        self._solidity = sc
        cmdutil = cmdutils()
        if enable:
            if sc == self._solidity:
                result = cmdutil.execCmd('solc --version')
                if result['status'] == 0:
                    self.sc_compiler = 'solc'
                else:
                    result = cmdutil.execCmd('solcjs --version')
                    if result['status'] == 0:
                        self.sc_compiler = 'solcjs'
                    else:
                        raise FileNotFoundError
            else:
                pass

    def compile(self, scFile, scName, output=None):
        if not output:
            output = os.path.join(GlobalCfg().dataDir(), scName)
        if not os.path.exists(output):
            os.mkdir(output)

        self.compile_params = self.compile_params.replace('scFile', scFile)
        self.compile_params = self.compile_params.replace('outputDir', output)

        if self.sc_compiler == 'solc':
            self.compile_params = ' --overwrite {0}'.format(
                self.compile_params)

        compile_cmd = self.sc_compiler + ' ' + self.compile_params

        return cmdutils().execCmd(compile_cmd)
