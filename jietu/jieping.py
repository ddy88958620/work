# mport re
#-*- coding: utf-8 -*-

import commands
import sys
import urllib2
import config
import MySQLdb
import json

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

def get_srcs(code_list):
    resp = urllib2.urlopen(mtv_api)
    js = json.loads(resp.read())
    src_list = []
    group_list = js["ChannelGroupList"]
    for g in group_list:
        for c in g["channelList"]:
            try:
                if c["stationCode"] in code_list:
                    src = {}
                    src["code"] = c["stationCode"]
                    src["url"] = c["streamings"][0]["url"]
                    src_list.append(src)
            except Exception, e:
                print e
                continue
    return src_list


def get_codes():
    conf = config.dbconfig
    conn = MySQLdb.connect(host=conf["host"], user=conf["user"], passwd=conf["passwd"],
                               db=conf["dbname"], port=conf["port"], charset=conf["charset"])
    cursor = conn.cursor()
    query = "SELECT code FROM "+conf['tbname']+" WHERE `snapshot` = 1"
    cursor.execute(query)
    codes = cursor.fetchall()
    code_list = []
    for c in codes:
        code_list.append(c[0])
    return code_list

def screenshot(url, pname):
    command = "/mnt/hgfs/Work/ffmpeg -i '%s' -f image2 -ss 1 -s '250x180' -vframes 1 '%s' -y" % (url, pname)
    status = commands.getoutput(command)
    return status

def main():
    code_list = get_codes()
    src_list = get_srcs(code_list)
    print len(src_list)
    for c in src_list:
        screenshot(c["url"], c["code"]+".jpg")
        print c["code"], "finished."

if __name__ == "__main__":
    main()
