#!/usr/bin/python
# -*- coding:utf-8 -*-

import pycurl


class Curl():
    def __init__(self):
        self.instance = pycurl.Curl()

    def enableDebug(self):
        self.instance.setopt(self.instance.VERBOSE, True)

    def __call__(self, url, Debug=False):

        self.instance.setopt(self.instance.URL, url)
        self.instance.setopt(self.instance.FOLLOWLOCATION, True)

        if Debug:
            self.enableDebug()

        self.instance.perform()

    def close(self):
        if self.instance:
            self.instance.close()

    def status(self):
        return self.instance.getinfo(self.instance.RESPONSE_CODE)

    def time(self):
        return self.instance.getinfo(self.instance.TOTAL_TIME)

    def version(self):
        return pycurl.version