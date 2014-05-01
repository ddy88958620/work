#!/usr/bin/env python
# -*- coding=utf-8 -*-

import urllib2
import xml.dom.minidom
import utils


def source_7po():

    s = utils.Sql()
    query = "INSERT INTO 7po_source(channel, url) VALUES(%s, %s, %s)"

    response = urllib2.urlopen("http://zb.7po.com/interface.php")
    dom = xml.dom.minidom.parseString(response.read())
    root = dom.documentElement
    channels = root.getElementsByTagName("channel")

    for channel in channels:
        channel_name = channel.getAttribute('name')
        for urlNode in channel.childNodes:
            url = urlNode.firstChild.wholeText
            params = (channel_name, url)
            s.insert(query, params)

    s.close()


def main():
    source_7po()

if __name__ == "__main__":
    main()
