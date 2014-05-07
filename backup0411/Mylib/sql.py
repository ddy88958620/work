#!/usr/bin/env python
# -*- coding=utf-8 -*-

import MySQLdb
import config

class Sql():
    def __init__(self, db_name):
        self.conn = MySQLdb.connect(host=config.host, user=config.user, passwd=config.passwd, db=config.db[db_name], port=config.port, charset=config.charset)
        self.cursor = self.conn.cursor()

    def insert(self, query, params):
        self.cursor.execute(query, params)
        self.conn.commit()

    def search(self, query):
    	self.cursor.execute(query);
    	fetch = self.cursor.fetchall()
    	return fetch

    def close(self):
    	self.cursor.close()
        self.conn.close()