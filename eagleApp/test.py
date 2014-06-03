#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web
import config
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

db = web.database(dbn="mysql", db=config.db, user=config.user, pw=config.passwd)

with open("log.txt", "w") as f:
    pass

results = db.select("live_channel", what="id, name", where="name LIKE '%成人%'")
for r in results:
    chid = r.id
    ch_name = r.name
    s_vars = {"chid": chid}
    srcs = db.select("live_source", what="playurl", vars=s_vars, where="id=$chid")
    for src in srcs:
        url = src.playurl
        with open("log.txt", "a+") as f:
            f.write("".join(["Channel: ", ch_name, " Url: ", url])
