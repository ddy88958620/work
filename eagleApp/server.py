#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import web
import json
import config
import hashlib

# web.config.debug = False
LIVE_IMG_DOMIN = "http://eagleapp.qiniudn.com"

render = web.template.render("templates/")

urls = (
    "/login", "login",
    "/index.html", "index",
    "/picture.html", "picture",
    "/live.html", "live",
    "/recommend.html", "recommend",
    "/logout", "logout",
    "/listdata", "listdata",    # 应用列表
    "/app_edit", "appEdit",
    "/app_delete", "appDelete",
    "/app_classify", "appClassify",
    "/recommend_edit", "recommendEdit",
    "/recommend_delete", "recommendDelete",
    "/recommend_build", "recommendBuild",
    "/live_edit", "liveEdit",
    "/live_delete", "liveDelete",
    "/live_build", "liveBuild",
    "/live_classify", "liveClassify",
    "/pic_list", "picList",
    "/start_pic", "startPic",   # 启动页图片接口
    "/load_pic", "loadPic", # 加载页图片接口
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

db = web.database(dbn="mysql", db=config.db, user=config.user, pw=config.passwd)

def logged():
    if session.loggedin == True:
        return True
    else:
        return False

def existed(user, pw):
    pwhash = hashlib.md5(pw).hexdigest()
    user_vars = {"user": user, "pw": pwhash}
    exist = db.select("users", vars=user_vars, where="uname=$user and passwd=$pw")
    return exist

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
        exist = existed(user, pw)
        if exist:
            session.loggedin = True
            session.user = user
            # web.ctx.status = 200
            data = json.dumps({"status": 200})
        else:
            # web.ctx.status = 403
            data = json.dumps({"status": 403})

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

class listdata():
    def GET(self):
        #score, show, pic
        what = "name, icon, publishdate, version, download, fullinfo"

class appEdit():
    def POST(self):
        data = web.data()

class picList():
    def __init__(self):
        self.tname = "live_starting"

    def GET(self):
        what = "url, time, status, weight"
        results = db.select(self.tname, what=what)
        data = {}
        data["status"] = 200
        data["picData"] = []
        for i in results:
            item = {}
            item["pic"] = LIVE_IMG_DOMIN + i.url
            item["time"] = i.time.strftime("%Y-%m-%d %H:%M:%S")
            item["state"] = i.status
            item["weight"] = i.weight
            data["picData"].append(item)
        data = json.dumps(data)
        return data

# class loadPic():
#     def GET(self):
#         pic = startPic()
#         pic.tname = "live_loading"
#         data = pic.GET()
#         return data


if __name__ == "__main__":
    app.run()
