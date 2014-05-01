#!/usr/bin/env python
# -*- coding=utf-8 -*-

import time
import requests
import sql


def main():
    api_url = "http://qvod.togic.com/api/channels"
    payload = {"distributor": "togic",
               "package": "com_togic_livevideo",
               "versionCode": "47",
               "access_token": "71523a1f60274174930f7a1388ca286093f1c443",
               "deviceId": "6cfc3ab2-03a2-efe7-b76d-01924c48ff68"}
    r = requests.get(api_url, params=payload)
    channel_list = r.json()

    s = sql.Sql("epg")
    query = "INSERT INTO togic_source (channel, url) VALUES (%s, %s)"

    param_list = []
    for channel in channel_list:
        channel_name = channel["title"]
        url_list = channel["urls"]
        for url in url_list:
            if "http://live.togic.com" in url:
                token_url = url + "?access_token=" + payload["access_token"]
                param_list.append((channel_name, token_url))
            else:
                param_list.append((channel_name, url))

    s.executemany(query, param_list)
    s.close()

if __name__ == "__main__":
    main()
