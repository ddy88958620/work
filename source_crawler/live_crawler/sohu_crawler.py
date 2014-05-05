
# -*- coding:utf-8 -*-

import sys
import utils
import handlesrc
import json
import time
import random

reload(sys)
sys.setdefaultencoding("utf-8")

channel_error = "Can not get channel information! -->"

channels_url = "http://tvimg.tv.itc.cn/live/stations.jsonp"
api = 'http://live.tv.sohu.com/live/player_json.jhtml?encoding=utf-8&lid=%s&ver=21&type=1&g=8&t=%f'
# live_url = "live.tv.sohu/"
# live_data_url = "http://live.tv.sohu.com/live/player_json.jhtml"


# def get_url(cid):
#     try:
#         payload = {"lid": cid, "type": "1"}
#         r = requests.get(live_data_url, params=payload)
#         live_info = r.json()
#     except Exception, e:
#         print live_error, e
#         return None
#
#     try:
#         live_url = live_info["data"]["live"]
#         r = requests.get(live_url)
#         url_info = json.loads(r.text)
#         result_url = url_info["url"]
#     except Exception, e:
#         print url_error % live_info["data"]["tvName"], e
#         return None
#
#     return result_url

# 获取直播频道信息列表
def get_clist():
    try:
        js = utils.get_json(channels_url, pattern="par=(.*?);")
        channnel_list = js["STATIONS"]
        return channnel_list
    except Exception, e:
        print channel_error, e
        exit(1)


def get_code(name):
    with open("code.json", "r") as f:
        js = json.loads(f.read())

    for category in js.values():
        for c in category:
            if name in c:
                return c[0]
    else:
        return False


def get_cinfo(c_list):
    src_list = []

    for channel in c_list:
        # 频道名
        cname = channel["STATION_NAME"]
        code = get_code(cname)
        # 如果IsSohuSource字段等于2则该频道的源来自cntv，且会自动跳转到cntv
        if 1 == channel["IsSohuSource"] and code:
            try:
                print "getting url from %s" % code

                # 频道ID
                cid = channel["STATION_ID"]
                t = random.uniform(1, 10)
                url = api % (cid, t)
                data = utils.get_json(url)

                src = {}
                src['code'] = code
                src['hls'] = data['data']['hls']
                src_list.append(src)

            except Exception, e:
                print e
            else:
                pass
            finally:
                pass
                time.sleep(1)
        else:
            continue

    return src_list

def main():
    print "start running sohu crawler...."

    c_list = get_clist()
    src_list = get_cinfo(c_list)
    handler = handlesrc.HandleSrc()
    handler.update(src_list, "sohu")

if __name__ == "__main__":
    main()
