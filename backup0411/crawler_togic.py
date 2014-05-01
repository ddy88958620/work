#!/usr/bin/env python
# -*- coding=utf-8 -*-

import time
from Mylib import sql
from Mylib import easyurl


def crawler_togic():
    api_url = "http://qvod.togic.com/api/channels?package=com_togic_livevideo&versionCode=45&access_token=0f5efcd34fe82e1733b37310394efb758babd1a8&deviceId=705ade98-4dd5-e865-db03-f3d19c0ba764"
    url_handler = easyurl.EasyUrl(api_url)
    channel_list = url_handler.get_json()

    s = sql.Sql()
    query = "INSERT INTO togic_source (channel, url) VALUES (%s, %s)"

    for channel in channel_list:
        channel_name = channel["title"]
        url_list = channel["urls"]
        for url in url_list:
            if "http" not in url:
                file_object = open("rtmp_source.txt", "w")
                file_object.write(url)
                file_object.close()
            elif "http://live.togic.com" in url:
                url = url + \
                    "?access_token=0f5efcd34fe82e1733b37310394efb758babd1a8"
                check_handler = easyurl.EasyUrl(url)
                result_url = check_handler.check_url(3)
                params = (channel_name, result_url)
                s.insert(query, params)
            else:
                check_handler = easyurl.EasyUrl(url)
                result_url = check_handler.check_url(3)
                params = (channel_name, result_url)
                sql.insert(query, params)

            time.sleep(0.5)

    sql.close()

if __name__ == "__main__":
    crawler_togic()
