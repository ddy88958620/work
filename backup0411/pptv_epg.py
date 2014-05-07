#!/usr/bin/env python
#-*- coding: utf-8 -*-

# ipd-ug: Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10
# 返回城市对应频道json的url"http://live.pptv.com/api/tv_list?cb=load.cbs.cb%s&area_id=%s&canBack=0"

import re
import sys
import json
import urllib
import urllib2
from Mylib import sql

reload(sys)
sys.setdefaultencoding("utf-8")

opener = urllib2.build_opener()
opener.addheaders = [
    ("User-Agent", "Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10")]
urllib2.install_opener(opener)


def find_areas(index_url, area_pattern):
    try:
        index_resp = urllib2.urlopen(index_url).read()
        #area_list结构((area_id, 城市), ...)
        area_list = re.findall(area_pattern, index_resp)
    except Exception, e:
        print e
        return False
    return area_list if area_list else False


def find_channels(area, url, json_pattern, channel_link_pattern, channel_name_pattern):
    try:
        # 获取地区中频道列表的url
        channel_url = url % (area[0], area[0])
        channel_resp = urllib2.urlopen(channel_url).read()
        channel_match = re.findall(json_pattern, channel_resp)[0]
        channel_json = json.loads(channel_match)
        # 获取含有频道列表的html
        channel_html = channel_json["html"]
        channel_link = re.findall(channel_link_pattern, channel_html)
        channel_name = re.findall(channel_name_pattern, channel_html)

        channel_dict = {}
        if channel_name:
            for i in xrange(len(channel_name)):
                channel_dict[channel_name[i]] = channel_link[i]
                print channel_name[i], channel_link[i]
        else:
            raise Exception
    except Exception, e:
        print e
        return False
    return channel_dict


def get_epg(epg_pattern)

# def find_channel_info(channel_link, vid_pattern, ctx_pattern, kk_pattern):
#     try:
#         vid_response = urllib2.urlopen(channel_link).read()
#         vid = re.findall(vid_pattern, vid_response)[0]
#         ctx = re.findall(ctx_pattern, vid_response)[0]
#         kk = re.findall(kk_pattern, urllib.unquote(ctx))[0]
#     except Exception, e:
#         print e
#         return False
#     return (vid, kk)

    #result_url = "http://web-play.pptv.com/web-m3u8-%s.m3u8?type=m3u8.web.pad&playback=0&kk=%s" % (vid, result_ctx)


def crawler_pptv(area_pattern, json_pattern, channel_link_pattern, channel_name_pattern, vid_pattern, ctx_pattern, kk_pattern):
    s = sql.Sql()
    query = "INSERT INTO pptv_source (channel, url, vid, ctx) VALUES (%s, %s, %s,  %s )"
    index_url = "http://live.pptv.com/list/tv_list"
    channel_url = "http://live.pptv.com/api/tv_list?cb=load.cbs.cb%s&area_id=%s&canBack=0"

    area_list = find_areas(index_url, area_pattern)
    if area_list:
        for area in area_list:
            channel_dict = find_channels(
                area, channel_url, json_pattern, channel_link_pattern, channel_name_pattern)
            if channel_dict:
                for channel_name in channel_dict:
                    # vid_kk = find_channel_info(channel_dict[channel_name], vid_pattern, ctx_pattern, kk_pattern)
                    # result_url = "http://web-play.pptv.com/web-m3u8-%s.m3u8?type=m3u8.web.pad&playback=0&kk=%s" % (vid, result_ctx)
                    # insert_info = (channel_name, channel_dict[channel_name])+vid_kk
                    # query = sql_query % insert_info
                    # sql.insert(query)
            else:
                print area[1], "has no channel"
    else:
        print "get area list failure"
        return False
    sql.close()
    return True


def main():
    area_pattern = re.compile(
        r'''<a\s+href="#"\s+area_id\s="(\d+)">(.*?)</a>''')
    json_pattern = re.compile(r'''load.cbs.cb\d+\((.*)\)''')
    #channel_link_pattern = re.compile(r'''_siteyydata ="(.*)"class=''')
    channel_link_pattern = re.compile(
        r'''<td class="show_playing"><a\s+href="(.*?)".*?>''')
    channel_name_pattern = re.compile(r'''</i><a href=.*?>(.*?)</a></td>''')
    vid_pattern = re.compile(r'''"vid":(\d+)''')
    ctx_pattern = re.compile(r'''"ctx":"(.*?)"''')
    kk_pattern = re.compile(r'''kk=(.*)''')

    if crawler_pptv(area_pattern, json_pattern, channel_link_pattern, channel_name_pattern, vid_pattern, ctx_pattern, kk_pattern):
        return True
    else:
        return False

if __name__ == '__main__':
    if main():
        print "Successfully!"
    else:
        print "Failure, try again."
