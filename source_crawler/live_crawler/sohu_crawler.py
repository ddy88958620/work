
# -*- coding:utf-8 -*-

import sys
import requests
import json
import re
import utils
import handlesource

reload(sys)
sys.setdefaultencoding("utf-8")

json_pattern = re.compile(r"par=(.*?);")

channel_error = "Can not get channel information! -->"
live_error = "Can not get live information! -->"
url_error = "Can not get live url of %s! -->"

channel_list_url = "http://tvimg.tv.itc.cn/live/stations.jsonp"
live_url = "live.tv.sohu/"
#live_data_url = "http://live.tv.sohu.com/live/player_json.jhtml"


# 获取直播频道信息列表
def get_clist():
    try:
        r = requests.get(channel_list_url)
        json_string = re.search(json_pattern, r.text).group(1)
        js = json.loads(json_string)
        channnel_list = js["STATIONS"]
        return channnel_list
    except Exception, e:
        print channel_error, e
        exit(1)


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


def main():
    info_list = get_clist()
    s = utils.Sql()
    for channel in info_list:
        # 频道ID
        cid = channel["STATION_ID"]
        # 频道名
        cname = channel["STATION_NAME"]
        handler = handlesource.HandleSource(cname, "sohu", s)
        # 如果IsSohuSource字段等于2则该频道的源来自cntv，且会自动跳转到cntv
        if 1 == channel["IsSohuSource"]:
            url = live_url + str(cid)
            print cname, url
            handler.update(url)
        else:
            continue
    s.close()

if __name__ == "__main__":
    main()
