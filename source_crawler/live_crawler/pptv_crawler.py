#!/usr/bin/env python
#-*- coding: utf-8 -*-

import re
import sys
import json
import utils
import handlesrc

reload(sys)
sys.setdefaultencoding("utf-8")

headers = [
    ("User-Agent", "Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10")]


# 匹配地区列表
area_pattern = re.compile(r'''<a\s+href="#"\s+area_id\s="(\d+)">(.*?)</a>''')
# 从返回的json中提取真正的json对象
json_pattern = re.compile(r'''load.cbs.cb\d+\((.*)\)''')
# 匹配频道url
url_pattern = re.compile(r'''<td class="show_playing"><a\s+href="(.*?)".*?>''')
# 匹配频道名
c_name_pattern = re.compile(r'''</i><a href=.*?>(.*?)</a></td>''')
# 匹配频道ID
vid_pattern = re.compile(r'''"vid":(\d+)''')
# ctx_pattern = re.compile(r'''"ctx":"(.*?)"''')
# kk_pattern = re.compile(r'''kk=(.*)''')
# url_pattern = re.compile(r'''_siteyydata ="(.*)"class=''')

area_error = "Can not get area list from area url --->"
area_none = "Can not match area list."
no_channel = "%s has no channel."
no_vid = "Can not get vid of %s"


# 获取地区列表
def get_areas(area_url):
    try:
        resp = utils.get_html(area_url)
    except Exception, e:
        print area_error, e
        exit(1)
    #area_list结构((area_id, 城市), ...)
    area_list = re.findall(area_pattern, resp)
    if not area_list:
        exit(area_none)
    else:
        return area_list


# 获取频道列表
def get_channels(area, url):
    try:
        # 获取地区中所有频道的url
        c_url = url % (area[0], area[0])
        resp = utils.get_html(c_url)
        c_match = utils.get_json(resp, json_pattern)
        # c_match = re.search(json_pattern, r.text).group(1)
        c_json = json.loads(c_match)
        # 获取含有频道列表的html
        c_html = c_json["html"]
        # 频道url列表
        urllist = re.findall(url_pattern, c_html)
        # 频道名列表
        namelist = re.findall(c_name_pattern, c_html)

        # 频道字典，频道名与url对应
        c_dict = {}
        for i in xrange(len(namelist)):
            c_dict[namelist[i]] = urllist[i]

    except Exception, e:
        print e
        return None
    else:
        return c_dict


# def get_channel_info(channel_link):

#     try:
#         r = requests.get(channel_link)
#         vid = re.findall(vid_pattern, r.text)[0]
#         ctx = re.findall(ctx_pattern, r.text)[0]
#         kk = re.findall(kk_pattern, urllib.unquote(ctx))[0]
#     except Exception, e:
#         print e
#         return False
#     return (vid, kk)


# 获取频道ID
def get_vid(channel_link):
    try:
        r = requests.get(channel_link)
        vid = re.findall(vid_pattern, r.text)[0]
        return vid
    except Exception, e:
        print e
        return None


def main():
    area_url = "http://live.pptv.com/list/tv_list"
    c_url = "http://live.pptv.com/api/tv_list?cb=load.cbs.cb%s&area_id=%s&canBack=0"

    # 地区列表
    area_list = get_areas(area_url)
    src_list = []
    for area in area_list:
        c_dict = get_channels(area, c_url)
        if c_dict:
            for name in c_dict:
                src= {}
                # vid_kk = get_channel_info(channel_dict[name])
                vid = get_vid(c_dict[name])
                if vid:
                    url = c_dict[name] + "?" + "vid=" + vid
                    src["url"] = url
                    print name, url
                else:
                    print no_vid % name
                    continue
                # param_list.append(
                #     (name, channel_dict[name]) + vid_kk)
        else:
            print no_channel % area[1]
            continue

    return

if __name__ == '__main__':
    main()
