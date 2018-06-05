#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import time
import unittest

import fs.path

from configuration.globalcfg import GlobalCfg
from lib import HTMLTestRunner
from lib.file.fileutils import comutils
from lib.file.properties import Properties


def _getSuite(startDir, pattern):
    _testSuite = []

    globalcfg = GlobalCfg()
    test_home = globalcfg.caseDir()

    if not startDir:
        startDir = test_home

    if pattern == 'test*.py':
        for caseFile in comutils().filterfiles(startDir, 'test*.py'):
            _testSuite.append(
                unittest.defaultTestLoader.discover(
                    start_dir=startDir, pattern=fs.path.basename(caseFile)))
    else:
        _testSuite = unittest.defaultTestLoader.discover(
            start_dir=startDir, pattern=pattern)

    return unittest.TestSuite(_testSuite)


def Run(startDir=None, testReg='test_transfer.py'):
    globalcfg = GlobalCfg()
    report_home = globalcfg.reportDir()

    if not startDir:
        startDir = None

    if not testReg:
        testReg = 'test*.py'

    suite = _getSuite(startDir, testReg)

    projectInfo = globalcfg.getProjectPInfo()
    os.mkdir(report_home, 755)
    reportname = os.path.join(report_home, 'TestResult.html')
    with open(reportname, 'wb') as f:
        runner = HTMLTestRunner.HTMLTestRunner(
            stream=f,
            title=u'{0}自动化测试报告'.format(projectInfo),
            description='{0} Automation testcase execution result'.format(
                projectInfo))
        runner.run(suite)

    time.sleep(3)

    # 发送邮件
    # mail = sendmail.SendMail()
    # mail.send()


if __name__ == '__main__':
    now = time.strftime('%Y_%m_%d_%H_%M_%S')
    globalcfg = GlobalCfg()
    runtime_Path = globalcfg.runtimeFile()
    runtime_Pro = Properties(runtime_Path)
    runtime_Pro.setProperties({'Start': now})
    Run(testReg='test_transfer.py')
