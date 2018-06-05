# coding=utf-8

import copy
import logging
import logging.config
import os
from collections import defaultdict

import yaml

from configuration.globalcfg import GlobalCfg


class Log:
    def __init__(self, name):
        self.name = name
        self.cfg = GlobalCfg().logcfgFile()
        self.logDir = GlobalCfg().reportDir()

    def _init_logger(self):
        with open(self.cfg, 'r') as fhandle:
            config = yaml.load(fhandle)

            # Update file name with correct log name
            log_item = defaultdict(dict)
            log_item = copy.deepcopy(config)

            log_item['handlers']['info_file_handler'][
                'filename'] = os.path.join(self.logDir, 'info.log')
            log_item['handlers']['error_file_handler'][
                'filename'] = os.path.join(self.logDir, 'errors.log')

            # Load Logging configuration
            logging.config.dictConfig(log_item)
            self.logger = logging.getLogger(self.name)

    def __printconsole(self, level, message):
        self._init_logger()

        # 记录一条日志
        if level == 'info':
            self.logger.info(message)
        elif level == 'debug':
            self.logger.debug(message)
        elif level == 'warning':
            self.logger.warning(message)
        elif level == 'error':
            self.logger.error(message)

    def debug(self, message):
        self.__printconsole('debug', message)

    def info(self, message):
        self.__printconsole('info', message)

    def warning(self, message):
        self.__printconsole('warning', message)

    def error(self, message):
        self.__printconsole('error', message)


if __name__ == '__main__':
    test_logger = Log(__name__)
    test_logger.info('Test')
