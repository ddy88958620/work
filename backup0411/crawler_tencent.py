#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Mylib import EasyUrl
from Mylib import sql
import re
import sys

reload(sys)
sys.setdefaultencoding("utf-8")


def regex_match(regex, text):
    pattern = re.compile(regex)
    match_list = re.findall(regex, text)
    return match_list


def crawler_tencent():
    channel_url = "http://v.qq.com/live/tv/list.html"
    url_handler = EasyUrl.EasyUrl(channel_url)
    chann_resp = url_handler.get_response()
    url_regex = r"<a _hot=\"live.tvlist.programlist\" href=\"(.*?)\" >"
    chan_regex = r"<span class=\"tv_name\">(.*?)</span>"
    id_regex = r"playid:'(\d+)',"

    s = sql.Sql()
    query = "INSERT INTO tencent_source(channel, url) VALUES('%s', '%s')"

    channel_list = regex_match(chan_regex, chann_resp)
    channel_urls = regex_match(url_regex, chann_resp)
    del channel_list[-1]

    channel_dict = {}
    for i in xrange(len(channel_urls)):
        channel_dict[channel_list[i]] = channel_urls[i]

    for channel in channel_list:
        url_handler = EasyUrl.EasyUrl(channel_dict[channel])
        id_resp = url_handler.get_response()
        play_id = regex_match(id_regex, id_resp)
        id_url = channel_dict[channel] + "?pid=" + play_id[0]
        print channel
        print id_url
        params = (channel, id_url)
        s.insert(query, params)

    sql.close()

if __name__ == "__main__":
    crawler_tencent()
