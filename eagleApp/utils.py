#!/usr/bin/env python
# -*- coding: utf-8 -*-

import config
import web
import hashlib
import sys


db = web.database(dbn="mysql", db=config.db, user=config.user, pw=config.passwd)

def signIn(user, pw):
    pwhash = hashlib.md5(pw).hexdigest()
    uid = db.insert("users", uname=user, passwd=pwhash)
    return uid

# def select():
#     db.select(, )

def main():
    if len(sys.argv) > 1:
        user = sys.argv[1]
        pw = sys.argv[2]
        signIn(user, pw)

if __name__ == "__main__":
    main()
    r = db.select("users")
    for i in r:
        print i.uname
    # conn = MySQLdb.connect(host=config.host, user=config.user, passwd=config.passwd,
    #                        db=config.db, port=config.port, charset=config.charset)
    # conn
