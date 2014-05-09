#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import web

render = web.template.render("templates/")

urls = (
    "/login", "login"
)


class login:
    def GET(self):
        return render.login()

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
