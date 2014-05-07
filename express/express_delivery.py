#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import sys
import urllib2

reload(sys)
sys.setdefaultencoding("utf-8")

opener = urllib2.build_opener()
opener.addheaders = [("User-Agent", "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36"),
                        ("Referer", "http://www.kuaidi100.com/auto.shtml")]
urllib2.install_opener(opener)

def get_info():
    code = raw_input("请输入你的快递单号： ")
    code_url = "http://www.kuaidi100.com/autonumber/auto?num=" + code
    firm_resp = urllib2.urlopen(code_url).read()
    #单号对应的可能的公司名列表
    firm_types = json.loads(firm_resp)

    if firm_types:
        valid = False
        for firm in firm_types:
            #"comCode"字段对应公司名
            firm_name = firm["comCode"]
            result_url = "http://www.kuaidi100.com/query?type=%s&postid=%s&id=1&valicode=&temp=0.7848867308348417" % (firm_name, code)
            info_resp = urllib2.urlopen(result_url).read()

            #返回的含有快递状态信息的json数据            
            result_data = json.loads(info_resp)
            #检查返回的快递状态信息是否有效
            if result_data["status"] == "200":
                for info in result_data["data"][::-1]:
                    #快递每一段的状态信息
                    print info["time"]
                    print info["context"]
                vaild = True
                break

        #所有可能的公司查询均失败，返回失败信息
        if valid:
            print "单号不存在或者已经过期"
    else:
        print "输入的快递单号有误"

if __name__ == '__main__':
    get_info()
