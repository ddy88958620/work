#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import utils
import checkdomin

reload(sys)
sys.setdefaultencoding("utf-8")

api_url = "http://live.91vst.com/list.php?v=top&app=vst&ver=1.0.0-D-20130816.0312"
api_error = "Can not get the information from vst api. --->"

def source_vst():
    urllist = []
    try:
        js = utils.get_html()
        info_dict = utils.get_json(js)

        for item in info_dict["live"]:
            url_list = item["urllist"].split("#")
            for url in url_list:
                urllist.append(url)

    except Exception, e:
        print api_error, e
        exit(1)

    return urllist


def main():
    urllist = source_vst()
    checker = checkdomin.CheckDomin("/root/live_crawler/vst_domin.json", "vst")
    checker.check(urllist)
    checker.send()

if __name__ == "__main__":
    main()
