#!/usr/bin/python
# -*- coding:utf-8 -*-


def paginate2json(inlist):
    result = []
    for item in inlist:
        result.append(item.__repr__())

    return result
