# mport re
#-*- coding: utf-8 -*-

import commands
import sys
import utils
import os
import live_probe

reload(sys)
sys.setdefaultencoding('utf8')


def getCodes():
    query = "SELECT code FROM mtv_channel WHERE `snapshot` = 1"
    s = utils.Sql()
    codes = s.select(query)
    code_list = []
    for c in codes:
        code_list.append(c[0])
    return code_list

def getSrcList(code):
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


def snapshot(url, pname):
    pic_name = "./tmp/"+pname
    cmd = "./ffmpeg -i '%s' -f image2 -ss 1 -s '250x180' -vframes 1 '%s' -y" % (url, pic_name)
    status = commands.getoutput(cmd)
    return status


def ifSnapFail(src_list, pname):
    success = False
    for src in src_list:
        url = src["url"]
        snapshot(url, pname)
        if not os.path.exists("./tmp"+pname):
            continue
        else:
            success = True

    if not success:
        print pname, "can not be created!"


def movePic():
    cmd = "mv ./tmp/* ./"
    status = commands.getoutput(cmd)
    print status


def main():
    code_list = getCodes()
    for code in code_list:
        src_list = getSrcList(code)
        url = selectBestUrl(code, src_list)
        pname = code + ".jpg"
        print snapshot(url, pname)
        if not os.path.exists("./tmp"+pname):
            ifSnapFail(src_list, pname)
        print code, "finished."
        break

    movePic()

if __name__ == "__main__":
    main()
