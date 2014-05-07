#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import urllib2
import json
from Mylib import sql

reload(sys)
sys.setdefaultcoding("utf-8")


def crawler_vst():
    response = urllib2.urlopen(
        "http://live.91vst.com/list.php?v=top&app=vst&ver=1.0.0-D-20130816.0312")
    info_dict = json.loads(response.read())

    channels = {}
    for program in info_dict["type"]:
        channels[program["id"]] = program["name"]

    s = sql.Sql()
    query = "INSERT INTO vst_source (channel_name, program, url) VALUES (%s, %s, %s)"

    for item in info_dict["live"]:
        if item["itemid"] in channels:
            channel_name = channels[item["itemid"][0]]
        else:
            channel_name = channels["8"]

        url_list = item["urllist"].split("#")
        for url in url_list:
            params = (channel_name, item["name"], url)
            s.insert(query, params)

    sql.close()

if __name__ == "__main__":
    crawler_vst()
