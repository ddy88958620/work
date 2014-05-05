#usr/bin/env python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import MySQLdb
import config

class Sql():
    def __init__(self):
        conf = config.dbconfig
        self.conn = MySQLdb.connect(host=conf["host"], user=conf["user"], passwd=conf["passwd"],
                               db=conf["dbname"], port=conf["port"], charset=conf["charset"])
        self.cursor = self.conn.cursor()

    def select(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result


def search(key, alist):
    for item in alist:
        if key in item:
            return item
    else:
        return False
