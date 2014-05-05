#!/usr/bin/env python
# -*- coding=utf-8 -*-

import sys
import MySQLdb
import config

reload(sys)
sys.setdefaultencoding("utf-8")

class HandleSrc:
    def __init__(self):
        self.config = config.dbconfig
        self.conn = MySQLdb.connect(host=self.config["host"], user=self.config["user"], passwd=self.config["passwd"],
                               db=self.config["dbname"], port=self.config["port"], charset=self.config["charset"])

    def update(self, src_list, site):
        if site == "cntv":
            self._update(src_list, "cntv", "auth")
            self._update(src_list, "cntv_hls", "hls")
            self._update(src_list, "cntv_flv", "flv")
            self.conn.close()
        if site == "sohu":
            self._update(src_list, "sohu", "hls")
        else:
            self._update(src_list, site, "url")
            self.conn.close()


    def _update(self, src_list, site, flag):
        cursor = self.conn.cursor()
        query = "replace into "+self.config["tbname"]+" (code, site, url, seq, status) values (%s, %s, %s, 1, 1)"
        for src in src_list:
            if flag in src:
                params = (src["code"], site, src[flag])
                cursor.execute(query, params)
            else:
                continue
