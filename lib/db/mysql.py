#!/usr/bin/python
# -*- coding:utf-8 -*-

import pymysql

from lib.db.database import DataBase


class Mysql(DataBase):
    def __init__(self, host, user, passwd, db, port=3306, charset='utf8'):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.db = db
        self.port = port if port else 3306
        self.charset = charset if charset else 'utf8'

    def conect(self):
        try:
            self.conn = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.passwd,
                database=self.db,
                charset=self.charset)
        except:
            raise ConnectionError('Connect Database Failed!!!')

        self.curs = self.conn.cursor()

    def insert(self, insert):
        try:
            effect_row = self.curs.execute(insert)
            self.conn.commit()
        except:
            self.conn.rollback()

        return effect_row

    def query(self, query):
        self.curs.execute(query)
        return self.curs.fetchall()

    def update(self, update):
        try:
            effect_row = self.curs.execute(update)
            self.conn.commit()
        except:
            self.conn.rollback()

        return effect_row

    def delete(self, delete):
        try:
            effect_row = self.curs.execute(delete)
            self.conn.commit()
        except:
            self.conn.rollback()

        return effect_row

    def callProc(self, proc, args):
        # Switch Cursor
        self.curs = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
        self.curs.callproc(proc, args=args)
        self.conn.commit()

        self.curs = self.conn.cursor()

    def execute(self, cmd):
        self.curs.execute(cmd)

    def close(self):
        if self.curs:
            self.curs.close()
        if self.conn:
            self.conn.close()


if __name__ == '__main__':
    mysql = Mysql('172.17.1.128', 'chenzc', 'chenzc', 'sp_test')
    mysql.conect()
    print(
        mysql.query(
            'SELECT A.address, A.id, B.score from blk_fortune_contract as A, fortune_forecast_event as B where A.address = B.address'
        ))
    mysql.close()
