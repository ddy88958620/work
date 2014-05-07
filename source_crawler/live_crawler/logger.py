#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# import sys
# import datetime
#
# reload(sys)
# sys.setdefaultencoding("utf-8")
#
# class Logger:
#     def __init__(self, source):
#         self.errorfile = "/root/live_crawler/log/error.txt"
#         self.outfile = "/root/live_crawler/log/output.txt"
#         self.source = source
#         self.now = datetime.datetime.now().strftime(" %Y-%m-%d %H:%M:%S")
#         with open(self.errorfile, "a+") as f:
#             f.write("\n" + self.source + self.now + "\n")
#         with open(self.outfile, "a+") as f:
#             f.write("\n" + self.source + self.now + "\n")
#
#     def log_exc(self, exce):
#         with open(self.errorfile, "a+") as f:
#             f.write(exce + "\n")
#
#     def log_out(self, output):
#         with open(self.outfile, "a+") as f:
#             f.write("\n" + self.source + self.now + "\n")
#             f.write(output + "\n")
