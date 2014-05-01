#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import json


def collect_rtmp():
    interface_url = "http://qvod.togic.com/api/channels?package=com_togic_livevideo&versionCode=45&access_token=9afc373b88ad1e6785765edea369034a3e6178e7&deviceId=705ade98-4dd5-e865-db03-f3d19c0ba764"
    request = urllib2.Request(interface_url)
    request.add_header(
        "User-Agent", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36")
    response = urllib2.urlopen(request)

    channel_list = json.loads(response.read())

    file_object = open("rtmp_source.txt", "w+")
    for channel in channel_list:
        channel_name = channel["title"]
        url_list = channel["urls"]
        for url in url_list:
            if url[:4] == "rtmp":
                file_object.write(url + "\n")

    file_object.close()


if __name__ == "__main__":
    collect_rtmp()
