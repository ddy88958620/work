#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import re
import smtplib
from email.mime.text import MIMEText
from email.header import Header

reload(sys)
sys.setdefaultencoding("utf-8")

pattern = re.compile(r'''(http|shttp|rtmp|rtsp)(://.*?)/''')

class CheckDomin:
    def __init__(self, fname):
        # 从文件中读取现有的域名列表
        with open(fname, "w") as f:
            self.old_set = set(json.loads(f.read()))

        self.sender = 'check_domin@163.com'
        self.receiver = 'zhangdongabbb@163.com'
        self.subject = 'new domins'
        self.smtpserver = 'smtp.163.com'
        self.username = 'check_domin'
        self.password = 'checkdomin'

    # 检查是否有新的域名出现
    def check(self, urllist):
        self.tmp_set = set([])
        for u in urllist:
            try:
                url = ''.join(re.search(pattern, u).groups())
                self.tmp_set.add(url)
            except AttributeError:
                continue


    # 发送邮件，内容为新添加的域名
    def __send_mail(self, domin_set):

        content = '\n'.join(domin_set)

        msg = MIMEText(content, 'plain', 'utf-8')  # 中文需参数‘utf-8’，单字节字符不需要
        msg['Subject'] = Header(self.subject, 'utf-8')
        msg['Sender'] = self.sender
        msg['From'] = self.sender
        msg['To'] = self.receiver

        smtp = smtplib.SMTP()
        smtp.connect(self.smtpserver)
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.set_debuglevel(1)
        smtp.login(self.username, self.password)
        smtp.sendmail(self.sender, self.receiver, msg.as_string())


    def send(self):
        new_set = self.tmp_set - self.old_set
        # 如果发现有新的域名则发送邮件
        if new_set:
            self.__send_mail(new_set)
        else:
            pass
