#!/usr/bin/env python
# -*- coding=utf-8 -*-

import MySQLdb
import config

class Sql():
    def __init__(self, db_name):
        self.conn = MySQLdb.connect(host=config.host, user=config.user, passwd=config.passwd, db=config.db[db_name], port=config.port, charset=config.charset)
        self.cursor = self.conn.cursor()

    def executemany(self, query, params):
        self.cursor.executemany(query, params)
        self.conn.commit()

    def execute(self, query, param):
        self.cursor.execute(query, param)
        self.conn.commit()

    def search(self, query, param):
        self.cursor.execute(query, param);
        fetch = self.cursor.fetchall()
        return fetch

    # def search(self, query, param):
    #     self.cursor.execute(query, param)
    #     fetch = self.cursor.fetchone()
    #     return fetch

    def close(self):
        self.cursor.close()
        self.conn.close()