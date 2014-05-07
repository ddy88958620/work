# -*- coding: utf-8 -*-

import utils

def get_code(name):
    with open("code.json", "r") as f:
        js = utils.get_json(f.read())

    for category in js.values():
        for c in category:
            if name in c:
                return c[0]

print get_code("浙江卫视")