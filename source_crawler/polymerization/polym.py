#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import urllib2
import json
from Mylib import sql

reload(sys)
sys.setdefaultencoding("utf-8")


def polymerization():
    query_7po = "SELECT channel FROM 7po_source"
    query_pptv = "SELECT channel FROM pptv_source"
    query_tencent = "SELECT channel FROM tencent_source"
    query_togic = "SELECT channel FROM togic_source"
    query_vst = "SELECT channel FROM vst_source"

    s = sql.Sql('epg')
    list_7po = list(s.search(query_7po))
    list_pptv = list(s.search(query_pptv))
    list_tencent = list(s.search(query_tencent))
    list_togic = list(s.search(query_togic))
    list_vst = list(s.search(query_vst))

    source_list = list(
        set(list_7po + list_pptv + list_tencent + list_togic + list_vst))
    source_list.sort()

    insert_query = "INSERT INTO channel (channel) VALUES (%s)"
    s = sql.Sql('source')
    for source in source_list:
        s.insert(insert_query, source)
    s.close()

polymerization()
