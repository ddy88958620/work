#!/usr/bin/env python
# -*- coding=utf-8 -*-

import urllib2
import json
import time
import re
import utils
from Mylib import easyurl


def check(checkurl):
    url = ""
    for i in xrange(3):
        result = True
        try:
            response = urllib2.urlopen(url=checkurl, timeout=3)
            response.close()
        except urllib2.HTTPError, e:
            result = False
        except urllib2.URLError, e:
            result = False
        except Exception, e:
            print e
        else:
            url = checkurl

        if result = True:
            return url

    return url


def source_cntv():
    channel_list = [
        "btv9", "btv3", "btv8", "btv7", "btv6", "btv2", "btv4", "cctvdoc", "cctvjilu", "shenzhen", "btv5", "jiangsu", "shandong", "xinjiang", "shan1xi", "dongfang", "btv1", "travel", "ningxia", "gansu", "xizang", "qinghai", "dongnan", "neimenggu", "guangdong", "jilin", "shan3xi", "hebei", "guangxi", "yunnan", "henan", "hubei", "guizhou", "heilongjiang", "chongqing",
        "sichuan", "jiangxi", "tianjin", "liaoning", "anhui", "hunan", "zhejiang", "cctv1", "cctv2", "cctv3", "cctv4", "cctv5", "cctv6", "cctv7", "cctv8", "cctv9", "cctv10", "cctv11", "cctv12", "cctv13", "cctv15", "cctv5plus", "cctvchild", "taiqiu", "taiqiu", "cctvgaowang", "cctvamerica", "cctvamerica", "cctveurope", "cctvfrench", "cctvarabic", "russian", "xiyu", "ipanda"]

    pattern = re.compile(r"html5VideoData\s+=\s+'(.*?)';")
    query = "INSERT INTO cntv_source(channel_name, hls1, hds2) VALUES(%s, %s, %s)"
    s = utils.Sql()

    for channel in channel_list:
        epg_url = "http://vdn.live.cntv.cn/api2/liveHtml5.do?channel=pa://cctv_p2p_hd%s&client=html5" % channel
        url_handler = easyurl.EasyUrl(epg_url)
        json_obj = url_handler.get_response()

        json_result = re.findall(pattern, response.read())
        info_dict = json.loads(json_result[0])

        if "hls_url" in info_dict:
            hls1_url = check(info_dict["hls_url"]["hls1"])
            hds2_url = check(info_dict["hds_url"]["hds2"])

            params = (channel, hls1_url, hds2_url)
            utils.insert(query, params)
            time.sleep(0.5)

    utils.close()


def main():
    source_cntv()

if __name__ == "__main__":
    main()
