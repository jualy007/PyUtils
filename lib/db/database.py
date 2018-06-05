#!/usr/bin/python
# -*- coding:utf-8 -*-

import abc

class DataBase(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def conect(self):
        pass

    @abc.abstractmethod
    def close(self):
        pass

