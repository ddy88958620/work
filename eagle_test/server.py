#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import web
import json

render = web.template.render("templates/")

urls = (
    "/login", "login",
    "/index", "index",
)


class login:
    def GET(self):
        return render.login()

    def POST(self):
        data = json.loads(web.data())
        if data["user"] == "shifenjiandan" and data["passwd"] == "123456":
            web.ctx.status = "200"
            data = json.dumps({"status": "200"})
            return data
        else:
            web.ctx.status = "403"

class index:
    def GET(self):
        return render.index()


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
