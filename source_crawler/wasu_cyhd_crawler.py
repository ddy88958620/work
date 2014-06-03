#!/usr/bin/env python
#-*- coding: utf-8 -*-

import httplib, urllib, urllib2
import json
import subprocess
import sys, os, re, time
import datetime
import src_manager
import traceback
import chardet

from comm import *
from urlparse import urlparse


reload(sys)
sys.setdefaultencoding("utf-8")



channel_list = {"中央一套": 'cctv1', "中央二套": 'cctv2', "中央三套": 'cctv3', "中央四套": 'cctv4', "中央五套": 'cctv5', "中央六套": 'cctv6', "中央七套": 'cctv7', "中央八套": 'cctv8', "中央九套": 'cctvjilu', "中央十套": 'cctv10', "中央十一套": 'cctv11', "中央十二套": 'cctv12', "中央新闻": 'cctv13', "中央少儿": 'cctvchild', "中央音乐": 'cctv15', "浙江卫视":'zhejiang', "湖南卫视":'hunan', "东方卫视":'dongfang', "江苏卫视":'jiangsu', "安徽卫视":'anhui', "北京卫视":'btv1', "深圳卫视":'shenzhen', "旅游卫视":'travel', "重庆卫视":'chongqing', "山东卫视":'shandong', "贵州卫视":'guizhou', "吉林卫视":'jilin', "天津卫视":'tianjin', "广东卫视":'guangdong', "黑龙江卫视":'heilongjiang', "东南卫视":'dongnan', "河南卫视":'henan', "陕西卫视":'shan3xi', "广西卫视":'guangxi', "云南卫视":'yunnan', "四川卫视":'sichuan', "湖北卫视":'hubei', "河北卫视":'hebei', "江西卫视":'jiangxi', "山西卫视":'shan1xi', "内蒙古卫视":'neimenggu', "宁夏卫视": 'ningxia', "新疆卫视": 'xinjiang', "西藏卫视": 'xizang', "青海卫视": 'qinghai', "甘肃卫视": 'gansu'}



api = 'http://html5-epg.wasu.tv/live/playback.shtml'





def cyhdwasu_run():
    print "start running cyhdwasu crawler...."

    src_list = []
    html = getHtml(api)

    try:
        print chardet.detect(html)
        jsn = html
        data = json.loads(jsn)

        fmt = "http://live.wasu.cn/%s.m3u8"

        for (group, channels) in data.items():            
            clist = channels['channelList']

            for item in clist:
                name = channel_list.get(item['channelName'])
                print item
                print item['channelName']
                print name

                if not name:
                    continue

                src = {}
                src['code'] = name
                url = item['playUrl']['httpUrl']
                code = match1(url, '.*/(.*)\.m3u8')
                src['hls'] = "http://live.wasu.cn/%s.m3u8" % code
                print src['hls']

                src_list.append(src)

    except Exception, e:
        print "%s" % traceback.format_exc()
    else:
        pass
    finally:
        pass

    return src_list


def main():
    srcs = cyhdwasu_run()
    # print srcs
    # manager = src_manager.Manager()
    # manager.update('cyhdwasu', srcs)

if __name__ == '__main__':
    main()