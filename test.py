#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

with open("live_channel.json", "r") as f:
    ch_data = json.loads(f.read())
    ch_list = ch_data["RECORDS"]

with open("live_source.json", "r") as f:
    src_data = json.loads(f.read())
    src_list = src_data["RECORDS"]

want_chs = []
for ch in ch_list:
    try:
        if "成人" in ch["name"]:
            print "***", ch["name"], "***"
            want_chs.append(ch)
    except Exception, e:
        print e
        continue

want_srcs = []
for src in src_list:
    for ch in want_chs:
        try:
            if src["chid"] == ch["id"]:
                print src["playurl"]
                want_srcs.append({"Channel": ch["name"], "Url": src["playurl"]})
        except Exception, e:
            print e
            continue

with open("want_srcs.json", "w+") as f:
    f.write(json.dumps(obj=want_srcs, ensure_ascii=False, indent=4))
