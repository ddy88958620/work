#!/usr/bin/env python
# -*- coding=utf-8 -*-

import requests
import xml.dom.minidom
import sys
from Mylib import sql
from Mylib import handlesource

reload(sys)
sys.setdefaultencoding("utf-8")

api_url = "http://zb.7po.com/interface.php"
to_error = "Timeout, try %d time"
chan_error = "Can not get channel information! --->"

def main():
    for i in range(3):
        try:
            r = requests.get(api_url, timeout=15)
        except Timeout, e:
            print to_error % (i + 1)
            continue
        except Exception, e:
            print chan_error, e
            exit(1)

    try:
        dom = xml.dom.minidom.parseString(r.text)
        root = dom.documentElement
        channels = root.getElementsByTagName("channel")
    except Exception, e:
        print chan_error, e
        exit(1)

    s = sql.Sql("source")
    for channel in channels:
        name = channel.getAttribute('name')
        handler = handlesource.HandleSource(name, "7po", s)
        for urlNode in channel.childNodes:
            url = urlNode.firstChild.wholeText
            handler.update(url)

    s.close()


if __name__ == "__main__":
    main()
