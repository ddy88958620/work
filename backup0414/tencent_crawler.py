#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from Mylib import sql
import re
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

url_regex = r"<a _hot=\"live.tvlist.programlist\" href=\"(.*?)\" >"
chan_regex = r"<span class=\"tv_name\">(.*?)</span>"
id_regex = r"playid:'(\d+)',"


def regex_match(regex, text):
    pattern = re.compile(regex)
    match_list = re.findall(regex, text)
    return match_list


def main():
    channel_url = "http://v.qq.com/live/tv/list.html"
    chann_resp = requests.get(channel_url)

    s = sql.Sql()
    query = "INSERT INTO tencent_source(channel, url) VALUES(%s, %s)"

    channel_list = regex_match(chan_regex, chann_resp)
    channel_urls = regex_match(url_regex, chann_resp)
    # 这里正则匹配得到频道列表时会多匹配一个标签，删除最后一个
    del channel_list[-1]

    channel_dict = {}
    for i in xrange(len(channel_urls)):
        channel_dict[channel_list[i]] = channel_urls[i]

    param_list = []
    for channel in channel_list:
        id_resp = requests.get(channel_dict[channel])
        play_id = regex_match(id_regex, id_resp)
        id_url = channel_dict[channel] + "?pid=" + play_id[0]
        print channel, id_url
        param_list.append((channel, id_url))

    s.executemany(query, param_list)
    s.close()

if __name__ == "__main__":
    main()
