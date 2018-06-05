#!/usr/bin/python
# -*- coding:utf-8 -*-

import os

from lib.file.properties import Properties


class GlobalCfg():
    def __init__(self):
        self.config_dir = os.path.dirname(__file__)
        self._home = os.path.join(self.config_dir, "..")
        self.cfg_Pro = Properties(
            os.path.join(self.config_dir, 'config.properties'))
        self.runtime_Pro = Properties(
            os.path.join(self.config_dir, 'runtime.properties'))

    def configDir(self):
        return self.config_dir

    def configFile(self):
        return os.path.join(self.config_dir, 'config.properties')

    def runtimeFile(self):
        return os.path.join(self.config_dir, 'runtime.properties')

    def logcfgFile(self):
        return os.path.join(self.config_dir, 'logger.yaml')

    def home(self):
        return self._home

    def startTime(self):
        return self.runtime_Pro.getProperty('Start')

    def getProjectPInfo(self):
        return self.cfg_Pro.getProperty('Project')

    def reportDir(self):
        return os.path.join(self._home, 'report', self.startTime())

    def dataDir(self):
        return os.path.join(self._home, 'data')

    def getContractDir(self):
        return os.path.join(self._home, 'contracts')

    def caseDir(self):
        return os.path.join(self._home, 'testcase')

    def gethHost(self):
        return self.cfg_Pro.getProperty('Host')

    def gethPort(self):
        return self.cfg_Pro.getProperty('Port')
