#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import web
import json
import config
import hashlib
import shutil
import os

# web.config.debug = False

LIVE_PIC_DOMIN = "http://eagleapp.qiniudn.com"
LIVE_PIC_DIR = "/static/live_uploads/"
TMP_DIR = "/static/tmp/"

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

# initializer = {
#     "loggedin": False,
#     "user": None
# }
# session = web.session.Session(app, web.session.DiskStore("sessions"), initializer=initializer)
# web.config.session_parameters['cookie_name'] = 'session_id'
# web.config.session_parameters["timeout"] = 300
# web.config.session_parameters["ignore_expiry"] = False
# web.config.session_parameters["ignore_change_ip"] = False

db = web.database(dbn="mysql", db=config.db, user=config.user, pw=config.passwd)

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
        what = "id, url, time, status, weight"

        if data_type.data == "starting":
            results = db.select(self.start_tab, what=what, order="status DESC, id")
        elif data_type.data == "loading":
            results = db.select(self.load_tab, what=what, order="status DESC, id")

        data = {}
        data["status"] = 200
        data["picData"] = []
        for r in results:
            item = {}
            item["id"] = r.id
            item["pic"] = r.url
            item["time"] = r.time.strftime("%Y-%m-%d %H:%M:%S")
            item["state"] = bool(r.status)
            item["weight"] = r.weight
            data["picData"].append(item)
        data = json.dumps(data)
        return data

    def POST(self):
        if logged():
            act = web.input().act
            input_data = json.loads(web.data())
            key = input_data["key"]
            data = json.loads(input_data["data"])

            if key == "starting":
                tab = self.start_tab
            elif key == "loading":
                tab = self.load_tab

            if act == "update":
                self._update(tab, data)
            elif act == "add":
                self._add(tab, data)
            elif act == "delete":
                self._delete(tab, data)

            return json.dumps({'status': 200})
        else:
            pass

    def _update(self, tab, data):
        domain = web.ctx.homedomain
        url = data["pic"]
        weight = data["weight"]
        if data["state"]:
            state = 1
        else:
            state = 0
        id = data["id"]
        where_vars = {"id": id}

        pic_name = url.split("/")[-1]
        tmp_dir = "".join([sys.path[0], TMP_DIR, pic_name])
        if os.path.exists(tmp_dir):
            new_dir = "".join([sys.path[0], LIVE_PIC_DIR])
            shutil.move(tmp_dir, new_dir)
            url = "".join([domain, LIVE_PIC_DIR, pic_name])

        db.update(tab, vars=where_vars, where="id=$id", url=url, status=state, weight=weight)

    def _add(self, tab, data):
        domain = web.ctx.homedomain
        url = data["pic"]
        weight = data["weight"]
        if domain in url:
            pic_dir = url.replace(domain, "")
            pic_name = pic_dir.split("/")[-1]
            tmp_dir = "".join([sys.path[0], pic_dir])
            new_dir = "".join([sys.path[0], LIVE_PIC_DIR])
            shutil.move(tmp_dir, new_dir)
            url = "".join([LIVE_PIC_DIR, pic_name])
        db.insert(tab, url=url, status=1, weight=weight)

    def _delete(self, tab, data):
        id = data
        where_vars = {"id": id}
        db.delete(tab, vars=where_vars, where="id=$id")


class livePicUpload:
    def POST(self):
        if logged():
            pic = web.input()
            pic_name = pic.Filename
            pic_data = pic.Filedata
            pic_path = "".join([sys.path[0], TMP_DIR, pic_name])
            with open(pic_path, "w") as f:
                f.write(pic_data)

            data = {}
            data["status"] = 200
            data["url"] = "".join([web.ctx.homedomain, TMP_DIR, pic_name])
            data = json.dumps(data)
        else:
            data = json.dumps({'status': 403})
            web.seeother(login_url)

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
