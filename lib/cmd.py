#!/usr/bin/python
# -*- coding:utf-8 -*-

import platform
import subprocess

from lib.log import Log


class cmdutils():
    logger = Log(__name__)

    def execCmd(self, cmd, shell=True):
        shell = (platform.system() == 'Linux')
        self.logger.info('Execute command: {0}'.format(cmd))
        proc = subprocess.Popen(
            cmd, shell=shell, stderr=subprocess.PIPE, stdout=subprocess.PIPE)

        status = proc.wait(timeout=120)

        # Convert to UTF-8
        proc_out = proc.stdout.read()

        try:
            out_str = str(proc_out, encoding='utf-8')
        except UnicodeDecodeError:
            out_str = str(proc_out, encoding='gbk')

        self.logger.info('Execute Status: {0}'.format(status))
        if not status:
            self.logger.error('Execute Output: {0}'.format(out_str))

        return {'status': status, 'message': out_str}


if __name__ == '__main__':
    test = cmdutils().execCmd('cmd.exe /c systeminfo', shell=False)
