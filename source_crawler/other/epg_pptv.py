#!/usr/bin/env python
#-*- coding: utf8 -*-

import re
import sys
import json
import urllib
import urllib2
import datetime
from Mylib import sql


reload(sys)
sys.setdefaultencoding("utf-8")

opener = urllib2.build_opener()
opener.addheaders = [("User-Agent",
                      "Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10")]
urllib2.install_opener(opener)

area_pattern = re.compile(r'''<a\s+href="#"\s+area_id\s="(\d+)">(.*?)</a>''')
json_pattern = re.compile(r'''load.cbs.cb\d+\((.*)\)''')
link_pattern = re.compile(
    r'''<td class="show_playing"><a\s+href="(.*?)".*?>''')
name_pattern = re.compile(r'''</i><a href=.*?>(.*?)</a></td>''')
# epg_json_pattern为节目单接口返回的json的pattern
epg_json_pattern = re.compile(r'''load.cbs.cbcb_\d+\((.*)\)''')
epg_pattern = re.compile(r'''</i>(.*?)</span>.*?>\s*.*?\stitle=.*?>(.*?)<''')
vid_pattern = re.compile(r'''"vid":(\d+)''')
ctx_pattern = re.compile(r'''"ctx":"(.*?)"''')
kk_pattern = re.compile(r'''kk=(.*)''')


# 获取地区列表
def get_areas(index_url):

    try:
        index_resp = urllib2.urlopen(index_url).read()
        # area_list结构((area_id, 城市), ...)
        area_list = re.findall(area_pattern, index_resp)
    except Exception, e:
        print e
        return False
    return area_list if area_list else False


# 获取相应地区的频道列表
def get_channels(area, url):

    try:
        # 获取地区中频道列表的url
        channel_url = url % (area[0], area[0])
        channel_resp = urllib2.urlopen(channel_url).read()
        channel_match = re.findall(json_pattern, channel_resp)[0]
        channel_json = json.loads(channel_match)
        # 获取含有频道列表的html
        channel_html = channel_json["html"]
        # 频道名列表
        channel_name = re.findall(name_pattern, channel_html)
        # 频道url列表
        channel_link = re.findall(link_pattern, channel_html)
        # 频道名和频道url一一对应的字典
        channel_dict = {}
        if channel_name:
            for i in range(len(channel_name)):
                channel_dict[channel_name[i]] = channel_link[i]
                # print channel_name[i], channel_link[i]
        else:
            raise Exception
    except Exception, e:
        print e
        return False
    return (channel_dict, channel_html)


def get_channel_info(channel_link):

    try:
        vid_response = urllib2.urlopen(channel_link).read()
        vid = re.findall(vid_pattern, vid_response)[0]
        ctx = re.findall(ctx_pattern, vid_response)[0]
        kk = re.findall(kk_pattern, urllib.unquote(ctx))[0]
    except Exception, e:
        print e
        return False
    return (vid, kk)


# 获取节目单，channel_html为抓取频道返回的json中提取的html串，
# today为当天的datetime.date.today()的实例
def get_epg(channel_id, channel_html, today):

    # cbcb表示是一周的第几天，date日期XXXX-XX-XX，id为channel id
    epg_url = 'http://live.pptv.com/api/tv_menu?cb=load.cbs.cbcb_%s&date=%s&id=%s&canBack=0'
    day = str(today)
    day_week = str(today.isoweekday())
    try:
        epg_response = urllib2.urlopen(epg_url %
                                       (day_week, day, channel_id)).read()
        epg_json = re.search(epg_json_pattern, epg_response).group(1)
        epg_html = json.loads(epg_json)['html']
        epg_list = re.findall(epg_pattern, epg_html)
    except Exception, e:
        print e
        return False
    return epg_list


def main():

    s = sql.Sql()
    sql_query = "INSERT INTO pptv_source (channel, url, vid, ctx) VALUES ('%s','%s','%s', '%s')"
    epg_query = "INSERT INTO pptv_epg (channel, time, program) VALUES ('%s', '%s', '%s')"
    index_url = "http://live.pptv.com/list/tv_list"
    channel_url = "http://live.pptv.com/api/tv_list?cb=load.cbs.cb%s&area_id=%s&canBack=0"
    today = datetime.date.today()

    area_list = get_areas(index_url)
    if area_list:
        for area in area_list:
            # area是一个元组(area id, area name)
            has_channel = get_channels(area, channel_url)

            if has_channel:
                (channel_dict, channel_html) = has_channel
                for channel_name in channel_dict:
                    vid_kk = get_channel_info(channel_dict[channel_name])
                    insert_info = (channel_name,
                                   channel_dict[channel_name]) + vid_kk
                    query = sql_query % insert_info
                    s.insert(query)
                    epg_list = get_epg(vid_kk[0], channel_html, today)
                    if epg_list:
                        for time, program in epg_list:
                            # print time, program
                            day_time = str(today) + ' ' + time
                            # print day_time
                            query = epg_query % (
                                channel_name, day_time, program)
                            s.insert(query)
                    else:
                        print channel_name, "has no epg."
            else:
                print area[1], "has no channel."
    else:
        print "get area list failure!"
        return False
    s.close()


if __name__ == '__main__':
    if main()
