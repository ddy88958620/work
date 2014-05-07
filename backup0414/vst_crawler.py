#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import requests
import sql

reload(sys)
sys.setdefaultencoding("utf-8")

api_url = "http://live.91vst.com/list.php"

def main():
    payload = {"v": "top",
               "app": "vst",
               "ver": "1.0.0-D-20130816.0312"}
    r = requests.get(api_url, params=payload)
    info_dict = r.json()

    channels = {}
    for program in info_dict["type"]:
        channels[program["id"]] = program["name"]

    s = sql.Sql("epg")
    query = "INSERT INTO vst_source (channel, url) VALUES (%s, %s)"
    param_list = []
    for item in info_dict["live"]:
        # if item["itemid"] in channels:
        #     category = channels[item["itemid"][0]]
        # else:
        #     category = "其他频道"

        url_list = item["urllist"].split("#")
        for url in url_list:
            param_list.append((item["name"], url))

    s.executemany(query, param_list)
    s.close()

if __name__ == "__main__":
    main()
