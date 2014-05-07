#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import re
import sys
import utils
import handlesource
import time

reload(sys)
sys.setdefaultencoding("utf-8")

api_error = "Can not get api information --->"
regex_error = "Regex pattern can not be matched --->"
chan_error = "Can not get details from %s --->"

# 匹配url
url_regex = r"<a _hot=\"live.tvlist.programlist\" href=\"(.*?)\" >"
# 匹配频道名
chan_regex = r"<span class=\"tv_name\">(.*?)</span>"
# 匹配playid
id_regex = r"playid:'(\d+)',"


# 获取匹配结果
def match(regex, text):
    pattern = re.compile(regex)
    match_list = re.findall(pattern, text)
    return match_list


def main():
    try:
        channel_url = "http://v.qq.com/live/tv/list.html"
        r = requests.get(channel_url)
        r.encoding = "utf-8"
    except Exception, e:
        print api_error, e
        exit(1)

    # 频道名列表
    c_list = match(chan_regex, r.text)
    # 频道url列表
    c_urls = match(url_regex, r.text)
    # 这里正则匹配得到频道列表时会多匹配一个标签，删除最后一个
    del c_list[-1]

    # 频道名与url一一对应的字典
    c_dict = {}
    for i in xrange(len(c_urls)):
        c_dict[c_list[i]] = c_urls[i]

    s = utils.Sql()
    for channel in c_list:
        try:
            r = requests.get(c_dict[channel])
            play_id = match(id_regex, r.text)
            # 将playid与url拼接
            url = c_dict[channel] + "?pid=" + play_id[0]
            handler = handlesource.HandleSource(channel, "tencent", s)
            handler.update(url)
            print channel, url
        except Exception, e:
            print chan_error % channel, e
            continue

    s.close()

if __name__ == "__main__":
    main()
