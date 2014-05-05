import httplib, urllib, urllib2
import json
import subprocess
import sys, os, re, time
import datetime
import random
import src_manager

from comm import *
from urlparse import urlparse


channel_list = {'anhui': 140, 'btv1': 307, 'chongqing': 294, 'dongfang': 74, 'dongnan': 224, 'gansu': 237, 'guangdong': 329, 'guangxi': 216, 'guizhou': 201, 'hebei': 100,
    'heilongjiang': 83, 'henan': 107, 'jiangxi': 173, 'jilin': 85, 'liaoning': 92, 'neimenggu': 266, 'ningxia': 243, 'qinghai': 865, 'shan1xitv': 116,
    'shan3xitv': 122, 'shandong': 131, 'shenzhen': 367, 'sichuan': 285, 'tianjin': 274, 'travel': 71, 'xiamen': 630, 'xinjiang': 253, 'xizang': 209, 'zhejiang': 147}


# channel_list = {'anhui': 140, 'btv1': 307}

api = 'http://live.tv.sohu.com/live/player_json.jhtml?encoding=utf-8&lid=%s&ver=21&type=1&g=8&t=%f'



def sohu_run():
    print "start running sohu crawler...."

    src_list = []
    for (code, vid) in channel_list.items():
        print "getting url from %s" % code

        try:
            t = random.uniform(1, 10)
            url = api % (vid, t)
            jsn = getHtml(url)
            # jsn = match1(jsn, '''html5VideoData\s*=\s*'(.*?)';''')
            data = json.loads(jsn)

            src = {}
            src['code'] = code
            src['hls'] = data['data']['hls']
            src_list.append(src)

        except Exception, e:
            print e
        else:
            pass
        finally:
            time.sleep(1)

    return src_list


def main():
    srcs = sohu_run()
    # print srcs
    manager = src_manager.Manager()
    manager.update('sohu_hls', srcs)

if __name__ == '__main__':
    main()