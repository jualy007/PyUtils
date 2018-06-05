#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import re
import shutil


class Properties:
    '''
    This class is using to process Properties File.
    '''

    _pfile = None

    _bakfile = None

    _fhandle = None

    _properties = {}

    def __init__(self, file_name):
        self._pfile = file_name
        self._properties = {}
        try:
            self._fhandle = open(self._pfile, 'r')
            for line in self._fhandle:
                line = line.strip()
                if line.find('=') > 0 and not line.startswith('#'):
                    strs = line.split('=')
                    self._properties[strs[0].strip()] = strs[1].strip()
        except Exception:
            raise Exception
        else:
            self._fhandle.close()

    def hasProperty(self, key):
        return self._properties.__contains__(key)

    def getProperty(self, key, default_value=''):
        _result = default_value

        if self._properties.__contains__(key):
            _result = self._properties.get(key)

            if _result.__contains__(','):
                _result = _result.split(',')

        return _result

    def setProperties(self, pro, overwrite=True):
        if overwrite == None:
            overwrite = True

        # Bakcup file before write properties
        self._bakfile = '{0}.bak'.format(self._pfile)
        shutil.copy(self._pfile, self._bakfile)

        # Read File
        self._fhandle = open(self._pfile, 'r')
        lines = self._fhandle.readlines()

        # Update or Add Properties
        for key, value in pro.items():
            old_value = self._properties.get(key)

            if old_value:
                from_reg = key + ' ?= ?.*'
                pattern = re.compile(r'' + from_reg)
                for index, line in enumerate(lines):
                    if pattern.search(
                            line) and not line.strip().startswith('#'):
                        if overwrite:
                            to_str = '{0} = {1}'.format(key, value)
                            lines[index] = re.sub(from_reg, to_str, line)
                        else:
                            to_str = '{0} = {1}'.format(
                                key, old_value + ', ' + value)
                            lines[index] = re.sub(from_reg, to_str, line)
            else:
                to_str = '{0} = {1}'.format(key, value)
                lines.append('\n' + to_str + '\n')

        self._fhandle.close()

        # Write Properties to file
        self._fhandle = open(self._pfile, 'w')
        self._fhandle.writelines(lines)
        self._close()

    def _close(self):
        if os.path.exists(self._bakfile):
            os.remove(self._bakfile)

        if self._fhandle:
            self._fhandle.close()


if __name__ == '__main__':
    pass
