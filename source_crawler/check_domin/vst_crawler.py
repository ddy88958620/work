#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import requests
from Mylib import sql
from Mylib import handlesource

reload(sys)
sys.setdefaultencoding("utf-8")

api_url = "http://live.91vst.com/list.php"

def main():
    s = sql.Sql("source")

    payload = {"v": "top",
               "app": "vst",
               "ver": "1.0.0-D-20130816.0312"}
    r = requests.get(api_url, params=payload)
    info_dict = r.json()

    param_list = []
    for item in info_dict["live"]:
        # item["name"]即url
        handler = handlesource.HandleSource(item["name"], "vst", s)
        url_list = item["urllist"].split("#")
        for url in url_list:
            # handler.set_params(url)
            handler.update(url)

    s.close()

if __name__ == "__main__":
    main()
