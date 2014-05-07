# mport re
#-*- coding: utf-8 -*-

import commands
import sys
import utils
import os
import urllib2
import config
import MySQLdb
import json
import live_probe

reload(sys)
sys.setdefaultencoding('utf8')

mtv_api = "http://vod.moretv.com.cn/Service/findChannelGroup?ver=2.1&areaCode=310100&ispCode=dianxin"

# def get_resolution(pattern, url):
#     result = commands.getoutput("/mnt/hgfs/Work/ffmpeg -i %s" % url)
#     print result
#     resolution = re.findall(pattern, result)
#     if resolution:
#         print resolution[0]
#         return resolution[0]
#     else:
#         return False


def getCodes():
    query = "SELECT code FROM mtv_channel WHERE `snapshot` = 1"
    s = utils.Sql()
    codes = s.select(query)
    code_list = []
    for c in codes:
        code_list.append(c[0])
    return code_list

def getSrcLIst(code):
    query = "SELECT (site, url) FROM mtv_source WHERE `code` = %s and status = 1"
    params = code
    s = utils.Sql()
    srcs = s.select(query, params=params)
    src_list = []
    for u in srcs:
        src = {}
        src["site"] = u[0]
        src["url"] = u[1]
        src_list.append(src)
    return src_list

def search(key, src_list):
    for src in src_list:
        if key in src["site"]:
            return src["url"]
    else:
        return False

def selectBestUrl(code, src_list):
    if "cctv" in code:
        url = search("cntv_flv", src_list)
        if url:
            return url
        else:
            url = src_list[0]["url"]
            live = live_probe.URLTranslater(url)
            real_url = live.realURL()
            return real_url
    else:
        qq_url = search("qq", src_list)
        sohu_url = search("sohu", src_list)
        ysten_url = search("ysten", src_list)
        other_url = src_list[0]["url"]

        if qq_url:
            real_url = live_probe.URLTranslater(qq_url).realURL()
            return real_url
        elif sohu_url:
            real_url = live_probe.URLTranslater(sohu_url).realURL()
            return real_url
        elif ysten_url:
            real_url = live_probe.URLTranslater(ysten_url).realURL()
            return real_url
        else:
            real_url = live_probe.URLTranslater(other_url).realURL()
            return real_url


def screenshot(url, pname):
    pic_name = "./tmp/"+pname
    command = "./ffmpeg -i '%s' -f image2 -ss 1 -s '250x180' -vframes 1 '%s' -y" % (url, pic_name)
    status = commands.getoutput(command)
    return status

def checkSnap(pname):
    pics = os.listdir("./tmp")
    if pname not in pics:
        print pname, "do not exist."


def main():
    code_list = getCodes()
    for code in code_list:
        src_list = getSrcLIst(code)
        url = selectBestUrl(code, src_list)
        print screenshot(url, code +".jpg")
        checkSnap(code+".jpg")
        print code, "finished."
        break

if __name__ == "__main__":
    main()
