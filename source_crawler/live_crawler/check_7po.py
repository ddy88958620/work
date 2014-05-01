#!/usr/bin/env python
# -*- coding=utf-8 -*-

import utils
import xml.dom.minidom
import checkdomin

api_url = "http://zb.7po.com/interface.php"

api_error = "Can not get the information from 7po api. --->"

# 从接口获取url列表
def source_7po():
    urllist = []
    try:
        resp = utils.get_html(api_url)
        dom = xml.dom.minidom.parseString(resp)
        root = dom.documentElement
        channels = root.getElementsByTagName("channel")

        for channel in channels:
            for urlNode in channel.childNodes:
                # 源的url
                url = urlNode.firstChild.wholeText
                urllist.append(url)

    except Exception, e:
        print api_error, e
        exit(1)

    return urllist


def main():
    urllist = source_7po()
    checker = checkdomin.CheckDomin("/root/live_crawler/7po_domin.json", "7po")
    checker.check(urllist)
    checker.send()

if __name__ == "__main__":
    main()
