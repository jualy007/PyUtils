#!/usr/bin/python
# -*- coding:utf-8 -*-

import requests

from lib.log import Log


class HttpRequest():
    '''
    Http Request lib
    '''

    def __init__(self, baseurl):
        self.baseurl = baseurl

    def request(self, option, path, header=None, data=None):
        option = option.strip().lower()
        url = self.baseurl + path

        if option == 'get':
            requests.get('')
        elif option == 'post':
            requests.post('')
        elif option == 'put':
            requests.put('')
        elif option == 'patch':
            requests.patch('')
        elif option == 'delete':
            requests.delete('')
        else:
            requests.request(option, '')