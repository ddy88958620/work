#!/usr/bin/env python
# -*- coding=utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import hashlib
import urllib2
import re
import json



def md5sum(text):
    m = hashlib.md5()
    m.update(text)
    return m.hexdigest()


def match(str, pattern):
    m = re.search(pattern, str)
    return m.group(1) if m else None

def matchall(str, pattern):
    m_list = re.findall(pattern, str)
    return m_list if m_list else None

def get_json(url, pattern=None, headers=None, data=None):
    js_string = get_html(url, headers, data)
    if pattern:
        js = json.loads(match(js_string, pattern))
    else:
        js = json.loads(js_string)
    return js


def get_html(url, headers=None, data=None):
    req = urllib2.Request(url)

    if headers:
        for key,value in headers.items():
            req.add_header(key,value)

    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
    response = opener.open(req, data)
    return response.read()