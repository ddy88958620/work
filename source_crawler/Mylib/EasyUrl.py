#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import urllib
import json
import sys
import re

reload(sys)
sys.setdefaultencoding("utf-8")


class EasyUrl:

    def __init__(self, url, headers={}, post_data=None):
        self.url = url
        if headers:
            self.headers = headers
        else:
            self.headers = {"User-Agent":
                            "Mozilla/5.1 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36"}

        if post_data:
            self.post_data = urllib.urlencode(post_data)
        else:
            self.post_data = post_data

    def get_response(self):
        self.req = urllib2.Request(
            url=self.url, data=self.post_data, headers=self.headers)
        self.response = urllib2.urlopen(self.req)
        return self.response.read()

    def get_json(self, json_pattern=None):
        json_response = self.get_response()

        if json_pattern:
            json_match = re.findall(json_pattern, json_response)
            if json_match:
                json_obj = json.loads(json_match[0])
            else:
                return False
        else:
            json_obj = json.loads(json_response)

        return json_obj

    def check_url(self, check_times=3, timeout=5):
        for i in xrange(check_times):
            print "**", i + 1, "**", self.url
            try:
                self.checked_result = urllib2.urlopen(
                    url=self.url, timeout=timeout)
                self.checked_result.close()
            except urllib2.HTTPError, e:
                print e.code, e
            except urllib2.URLError, e:
                print e
            except Exception, e:
                print e
            else:
                return self.url

        return ""
