#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import web
import json
import utils
import config
import hashlib

# web.config.debug = False
LIVE_PIC_DOMIN = "http://eagleapp.qiniudn.com"
LIVE_PIC_DIR = "static/live_uploads/"

render = web.template.render("templates/")

urls = (
    "/login", "login",
    "/index.html", "index",
    "/picture.html", "picture",
    "/live.html", "live",
    "/recommend.html", "recommend",
    "/logout", "logout",

    # 接口
    "/live_pic", "livePic",    # 直播配图
    "/live_pic_upload", "livePicUpload",    # 直播配图上传接口
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
    "/upload_test", "uploadTest",
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
        pass
        #score, show, pic
        # what = "name, icon, publishdate, version, download, fullinfo"

class appEdit():
    def POST(self):
        pass
        # data = web.data()

class livePic():
    def __init__(self):
        self.start_tab = "live_starting"
        self.load_tab = "live_loading"

    def GET(self):
        data_type = web.input()
        print data_type
        what = "url, time, status, weight"

        if data_type.data == "starting":
            results = db.select(self.start_tab, what=what, order="status DESC, id")
        elif data_type.data == "loading":
            results = db.select(self.load_tab, what=what, order="status DESC, id")

        data = {}
        data["status"] = 200
        data["picData"] = []
        for i in results:
            item = {}
            item["pic"] = LIVE_PIC_DOMIN + i.url
            item["time"] = i.time.strftime("%Y-%m-%d %H:%M:%S")
            item["state"] = bool(i.status)
            item["weight"] = i.weight
            data["picData"].append(item)
        data = json.dumps(data)
        return data

    def POST(self):
        data = web.input()


class livePicUpload:
    def POST(self):
        pic = web.input()
        pic_name = pic.Filename
        pic_data = pic.Filedata
        pic_path = "".join([LIVE_PIC_DIR, pic_name])
        # pic_path = "".join([LIVE_IMG_DOMIN, pic_name])
        with open(pic_path, "w") as f:
            f.write(pic_data)

        data = {}
        data["status"] = 200
        data["url"] = "http://210.73.218.156:57709/" + pic_path
        data = json.dumps(data)
        return data


class uploadTest:
    # def GET(self):
    #     x = web.input()
    #     web.debug(x)

    def POST(self):
        x = web.input()
        web.debug(x)

if __name__ == "__main__":
    app.run()
