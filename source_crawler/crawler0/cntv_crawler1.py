import httplib, urllib, urllib2
import json
import subprocess
import sys, os, re, time
import datetime
import src_manager

from comm import *
from urlparse import urlparse


channel_list = [
"btv9", "btv3", "btv8", "btv7", "btv6", "btv2", "btv4", "cctvdoc", "cctvjilu", "shenzhen", "btv5", "jiangsu", "shandong", "xinjiang", "shan1xi", "dongfang", "btv1", "travel", "ningxia", "gansu", "xizang", "qinghai", "dongnan", "neimenggu", "guangdong", "jilin", "shan3xi", "hebei", "guangxi", "yunnan", "henan", "hubei", "guizhou", "heilongjiang", "chongqing",
"sichuan", "jiangxi", "tianjin", "liaoning", "anhui", "hunan", "zhejiang", "cctv1", "cctv2", "cctv3", "cctv4", "cctv5", "cctv6", "cctv7", "cctv8", "cctv9", "cctv10", "cctv11", "cctv12", "cctv13", "cctv15", "cctv5plus", "cctvchild", "taiqiu", "cctvgaowang", "cctvamerica", "cctveurope", "cctvfrench", "cctvarabic", "ipanda"]

# channel_list = ["cctv1", "cctv2"]

api = 'http://vdn.live.cntv.cn/api2/live.do?channel=pa://cctv_p2p_hd%s'





def cntv_run():
    print "start running cntv crawler...."
    src_list = []
    for channel in channel_list:
        print "getting url from %s" % channel

        try:
            jsn = getHtml(api % channel)
            # jsn = match1(jsn, '''html5VideoData\s*=\s*'(.*?)';''')
            data = json.loads(jsn)

            src = {}
            src['code'] = channel
            src['hls'] = data['hls_url']['hls1']
            src['auth'] = data['hls_url']['hls2']
            src['flv'] = data['hds_url']['hds2']

            src_list.append(src)

        except Exception, e:
            print e
        else:
            pass
        finally:
            time.sleep(1)

    return src_list


def main():
    srcs = cntv_run()
    
    # print srcs
    # manager = src_manager.Manager()
    # manager.update('cntv_fix', srcs)

if __name__ == '__main__':
    main()