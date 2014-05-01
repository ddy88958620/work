#!/usr/bin/env python
# -*- coding: utf-8 -*-

######
# 不要想当然的把函数里的局部变量全部私有化！！！别随随便便就加self！！！
######

import json
import utils
import time
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

class OutputJson:
	def __init__(self, source_name):
		self.time_now = time.strftime("%Y-%m-%d %H: %M", time.localtime(time.time()))
		self.sql = utils.Sql()
		self.json_obj = {}

		self.json_obj["source_name"] = source_name
		self.json_obj["create_time"] = self.time_now
		self.json_obj["channel"] = []

	def __extract(self, table_name):
		query = "SELECT * FROM %s" % table_name
		result = self.sql.search(query)
		for channel in result:
			chann_dict = {}
			chann_dict["url_list"] = []
			chann_dict["channel_name"] = channel[1]
			chann_dict["url_list"].append(channel[2])
			self.json_obj["channel"].append(chann_dict)

	def out_put(self, table_name):
		self.__extract(table_name)
		json_output = json.dumps(obj=self.json_obj, ensure_ascii=False, indent=4)
		return json_output

if __name__ == '__main__':
	op = OutputJson("tencent")
	json_output = op.out_put("tencent_source")
	file_object = open("json_output.json", "w+")
	file_object.write(json_output)
	file_object.close()
