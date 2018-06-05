#!/usr/bin/python
# -*- coding:utf-8 -*-

import os

from configuration.globalcfg import GlobalCfg
from public.src.basictest import MyTest
from public.src.compile import Compile


class TestCompile(MyTest):
    def test_compile_guessgame(self):
        guessgame = os.path.join(GlobalCfg().getContractDir(), 'guessgame.sol')
        guessgame_compile = Compile(guessgame, 'GuessGame')
        guessgame_compile()
        self.assertTrue(guessgame_compile.status, 'Compile Contract Failed')
        self.assertTrue(os.path.exists(guessgame_compile.getABIPath()))
        self.assertTrue(os.path.exists(guessgame_compile.getCodePath()))

    def test_compile_guessgameoption(self):
        guessgameoption = os.path.join(GlobalCfg().getContractDir(),
                                       'guessgameoption.sol')
        guessgameoption_compile = Compile(guessgameoption, 'GuessGameOption')
        guessgameoption_compile()
        self.assertTrue(guessgameoption_compile.status,
                        'Compile Contract Failed')
        self.assertTrue(os.path.exists(guessgameoption_compile.getABIPath()))
        self.assertTrue(os.path.exists(guessgameoption_compile.getCodePath()))
