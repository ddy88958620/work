#!/usr/bin/env python
# -*- coding=utf-8 -*-

import requests
import xml.dom.minidom
from Mylib import sql


def main():
    s = sql.Sql()
    query = "INSERT INTO 7po_source(channel, url) VALUES(%s, %s, %s)"

    r = requests.get("http://zb.7po.com/interface.php")
    dom = xml.dom.minidom.parseString(r.text)
    root = dom.documentElement
    channels = root.getElementsByTagName("channel")

    param_list = []
    for channel in channels:
        channel_name = channel.getAttribute('name')
        for urlNode in channel.childNodes:
            url = urlNode.firstChild.wholeText
            param_list.append((channel_name, url))

    s.executemany(param_list)
    s.close()


if __name__ == "__main__":
    main()
