#!/usr/bin/python
# -*- coding:utf-8 -*-

import glob
import os

try:
    import cPickle as pickle
except ImportError:
    import pickle

from fs import open_fs
from lib.log import Log


class comutils():
    logger = Log(__name__)

    def fileReader(self, path):
        result = None

        try:
            fhandle = open(path, 'r')
            result = fhandle.read()
        finally:
            if fhandle:
                fhandle.close()

        return result

    def files(self, curr_dir='.', ext='*.exe'):
        """当前目录下的文件"""
        for i in glob.glob(os.path.join(curr_dir, ext)):
            yield i

    def all_files(self, rootdir, ext):
        """当前目录下以及子目录的文件"""
        for name in os.listdir(rootdir):
            if os.path.isdir(os.path.join(rootdir, name)):
                try:
                    for i in self.all_files(os.path.join(rootdir, name), ext):
                        yield i
                except:
                    pass
        for i in self.files(rootdir, ext):
            yield i

    def remove_files(self, rootdir, ext, show=False):
        """删除rootdir目录下的符合的文件"""
        for i in self.files(rootdir, ext):
            if show:
                self.logger.info('Delete File {0}'.format(i))
            os.remove(i)

    def remove_all_files(self, rootdir, ext, show=False):
        """删除rootdir目录下以及子目录下符合的文件"""
        for i in self.all_files(rootdir, ext):
            if show:
                self.logger.info('Delete File {0}'.format(i))
            os.remove(i)

    def clean(self, path):
        if os.path.exists(path):
            if os.path.isdir(path):
                os.removedirs(path)
            else:
                fhandle = open(path, 'w')
                fhandle.truncate()
                fhandle.close()
        else:
            pass

    def dump(self, keys, fHandle):
        pickle.dump(keys, fHandle)
        fHandle.close()

    def load(self, fHandle):
        result = pickle.load(fHandle)
        fHandle.close()
        return result

    def filterfiles(self, path, filter):
        if not isinstance(filter, list):
            fsfilter = [filter]

        fpath = open_fs(path)
        return fpath.walk.files(filter=fsfilter)