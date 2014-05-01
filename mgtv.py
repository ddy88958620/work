# -*- coding: utf-8 -*-

import urllib, urllib2
import json, hashlib, re, time, os, sys
import subprocess



fmt = 'http://interface.hifuntv.com/mgtv/BasicIndex/ApplyPlayVideo?Tag=26&BussId=4000004&VideoId=%s&VideoType=1&MediaAssetsId=TimeShift&CategoryId=1000009&VideoIndex=0&UserAgent=%s&Version=3.2.92.10.2.HMD.3.2_Release&ExData=%s&UserId=&MacId=&NetId=051616016033583'
ua = 'nn_player%2Fstd%2F1.0.0'
ter = 'terminal%3D%E6%B5%B7%E7%BE%8E%E8%BF%AA'


def getHtml(url, headers=None, data=None):
    req = urllib2.Request(url)

    if headers:
        for key,value in headers.items():
            req.add_header(key,value)

    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
    response = opener.open(req, data)
    return response.read()


def match1(str, pattern):
    m = re.search(pattern, str)
    if m:
        return m.group(1)


def parse(vid):
    xurl = fmt % (vid, ua, ter)
    xstr = getHtml(xurl)
    live_url = match1(xstr, 'url="(\S*?)"')
    return live_url


def main(i):
    with open("channel.json", "r") as f:
        channels = json.loads(f.read())
    with open(i+".txt", "w+") as f:
        for c in channels:
            channel = c.keys()[0]
            vid = match1(channel, '/(\w+)$')
            live_url = parse(vid)
            f.write(live_url+"\n")
            print live_url


if __name__ == '__main__':
    main("dianxintong")