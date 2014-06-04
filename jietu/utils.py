#usr/bin/env python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import MySQLdb
import config
import json
import threading

log_lock = threading.Lock()

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


class Logger():
    def __init__(self, code, log_file):
        self.code = code
        self.log_file = log_file
        self.log_data = {"code": self.code, "data_list": []}

    def log(self, level, url=None):

        '''
        level == 1: 截图完成
        level == 2: 错误
        level == 3: 截图失败
        '''

        data = {"url": url}
        if level == 1:
            data["state"] = "successful"
            self.log_data["data_list"].append(data)
            self.log_data["result"] = "Complete"
            self._log_complete()
        elif level == 2:
            data["state"] = "failed"
            self.log_data["data_list"].append(data)
        elif level == 3:
            data["state"] = "failed"
<<<<<<< HEAD
            # if url == None:
            #     self.log_data["result"] = "".join(["source list of ", self.code, "is empty"])
            # self.log_data["data_list"].append(data)
=======
>>>>>>> fcb98426123fb48a11c98028531885746774c98b
            self.log_data["result"] = "Can not snapshoted"
            self._log_complete()

    def _log_complete(self):
        data = json.dumps(obj=self.log_data, ensure_ascii=False, indent=4)
        log_lock.acquire()
        with open(self.log_file, "a+") as f:
            f.write("".join([data, "\n\n"]))
<<<<<<< HEAD
        log_lock.release()
=======
        log_lock.release()
>>>>>>> fcb98426123fb48a11c98028531885746774c98b
