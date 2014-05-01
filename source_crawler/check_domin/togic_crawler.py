#!/usr/bin/env python
# -*- coding=utf-8 -*-

import time
import requests
import sys
from Mylib import sql

reload(sys)
sys.setdefaultencoding("utf-8")

def main():
    api_url = "http://qvod.togic.com/api/channels"
    payload = {"package": "com_togic_livevideo",
               "versionCode": "45",
               "access_token": "0f5efcd34fe82e1733b37310394efb758babd1a8",
               "deviceId": "705ade98-4dd5-e865-db03-f3d19c0ba764"}
    r = requests.get(api_url, params=payload)
    channel_list = r.json()

    s = sql.Sql()
    query = "INSERT INTO togic_source (channel, url) VALUES (%s, %s)"

    for channel in channel_list:
        channel_name = channel["title"]
        url_list = channel["urls"]
        param_list = []
        for url in url_list:
            if "http" not in url:
                file_object = open("rtmp_source.txt", "w")
                file_object.write(url)
                file_object.close()
            elif "http://live.togic.com" in url:
                token_url = url + "?access_token=" + payload["access_token"]
                param_list.append((channel_name, token_url))
            else:
                check_handler = easyurl.EasyUrl(url)
                result_url = check_handler.check_url(3)
                param_list.append((channel_name, url))

            time.sleep(0.5)

    s.executemany(query, param_list)
    s.close()

if __name__ == "__main__":
    main()
