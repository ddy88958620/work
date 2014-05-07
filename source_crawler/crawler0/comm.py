import urllib, urllib2
import json, hashlib, re, time, os
import subprocess



def md5sum(text):
    m = hashlib.md5()
    m.update(text)
    return m.hexdigest()


def match1(str, pattern):
    m = re.search(pattern, str)
    if m:
        return m.group(1)


def getHtml(url, headers=None, data=None):
    req = urllib2.Request(url)

    if headers:
        for key,value in headers.items():
            req.add_header(key,value)

    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
    response = opener.open(req, data)
    return response.read()