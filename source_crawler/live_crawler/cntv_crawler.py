#!/usr/bin/env python
# -*- coding=utf-8 -*-

import json
import re
import utils
import handlesrc
import time

json_pattern = re.compile(r"html5VideoData\s+=\s+'(.*?)';")
chann_error = "Can not get name of %s. --->"
api_error = "Can not get information from api. --->"

channel_list = [
    "btv9", "btv3", "btv8", "btv7", "btv6", "btv2", "btv4", "cctvdoc", "cctvjilu", "shenzhen", "btv5", "jiangsu",
    "shandong", "xinjiang", "shan1xi", "dongfang", "btv1", "travel", "ningxia", "gansu", "xizang", "qinghai",
    "dongnan","neimenggu", "guangdong", "jilin", "shan3xi", "hebei", "guangxi", "yunnan", "henan", "hubei",
    "guizhou", "heilongjiang", "chongqing","sichuan", "jiangxi", "tianjin", "liaoning", "anhui", "hunan",
    "zhejiang", "cctv1", "cctv2", "cctv3", "cctv4", "cctv5", "cctv7", "cctv8", "cctv9", "cctv10", "cctv11",
    "cctv12", "cctv13", "cctv15", "cctv5plus", "cctvchild", "taiqiu", "cctvgaowang", "cctvamerica", "cctveurope",
    "cctvfrench", "cctvarabic", "ipanda"]

#api_html5 = 'http://vdn.live.cntv.cn/api2/liveHtml5.do?channel=pa://cctv_p2p_hd%s&client=html5'
api = 'http://vdn.live.cntv.cn/api2/live.do?channel=pa://cctv_p2p_hd%s'

#js_pattern = '''html5VideoData\s*=\s*'(.*?)';'''

def cntv_crawler(api):
    print "start running cntv crawler...."
    src_list = []
    for channel in channel_list:
        print "getting url from %s" % channel

        try:
            jsn = utils.get_html(api % channel)
            data = utils.get_json(jsn)
            src = {}
            src["code"] = channel
            src['auth'] = data['hls_url']['hls2']
            if "cctv" in channel:
                src["hls"] = data['hls_url']['hls1']
                src['flv'] = data['hds_url']['hds2']

            src_list.append(src)

        except Exception, e:
            print e
        else:
            pass
        finally:
            pass
            #time.sleep(1)

    return src_list

def main():
    src_list = cntv_crawler(api)
    handler = handlesrc.HandleSrc()
    handler.update(src_list, "cntv")


if __name__ == "__main__":
    main()