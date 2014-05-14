#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import web
import json
import config

# web.config.debug = False

render = web.template.render("templates/")

urls = (
    "/login", "login",
    "/index.html", "index",
    "/picture.html", "picture",
    "/live.html", "live",
    "/recommend.html", "recommend",
    "/logout", "logout"
)

login_url = "/login"
index_url = "/index.html"

app = web.application(urls, globals())

if web.config.get('_session') is None:
    initializer = {
        "loggedin": False,
        "user": None
    }
    session = web.session.Session(app, web.session.DiskStore("sessions"), initializer=initializer)
    web.config._session = session
    web.config.session_parameters['cookie_name'] = 'session_id'
    web.config.session_parameters["timeout"] = 300
    web.config.session_parameters["ignore_expiry"] = False
    web.config.session_parameters["ignore_change_ip"] = False
else:
    session = web.config._session


def logged():
    if session.loggedin == True:
        return True
    else:
        return False

def existed(user, pw):
    # query = "SELECT * FROM users WHERE uname=%s and passwd=%s"
    db = web.database(dbn="mysql", db=config.db, user=config.user, pw=config.passwd)
    user_vars = {"user": user, "pw": pw}
    exist = db.select("users", vars=user_vars, where="uname=$user and passwd=$pw", _test=True)
    if exist:
        return True
    else:
        return False

class login:
    def GET(self):
        if logged():
            raise web.seeother(index_url)
        else:
            return render.login()

    def POST(self):
        data = json.loads(web.data())
        user = data["user"]
        pw = data["passwd"]
        if existed(user, pw):
            session.loggedin = True
            session.user = user
            data = json.dumps({"status": "200"})
        else:
            data = json.dumps({"status": "403"})

        return data

class index:
    def GET(self):
        if logged():
            return render.index()
        else:
            raise web.seeother(login_url)


class picture:
    def GET(self):
        if logged():
            return render.picture()
        else:
            raise web.seeother(login_url)

class live:
    def GET(self):
        if logged():
            return render.live()
        else:
            raise web.seeother(login_url)

class recommend:
    def GET(self):
        if logged():
            return render.recommend()
        else:
            raise web.seeother(login_url)

class logout:
    def GET(self):
        session.kill()
        raise web.seeother(login_url)

if __name__ == "__main__":
    app.run()
