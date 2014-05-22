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
import datetime

# web.config.debug = False

LOAD_PIC_DIR = "/image/loading/"
START_PIC_DIR = "/image/splash/"
STATIC = "/static"
TMP_DIR = "/static/tmp/"
DOMAIN = "http://eagleapp.tv:57709"

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
    exist = db.select("admin", vars=user_vars, where="uname=$user and passwd=$pw")
    return exist

# def redirect():
#     web.seeother(login_url)

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
            data = json.dumps({"status": 200})
        else:
            data = json.dumps({"status": 403})

        return data

class index:
    def GET(self):
        if logged():
            return render.index(session.user)
        else:
            raise web.seeother(login_url)


class picture:
    def GET(self):
        if logged():
            return render.picture(session.user)
        else:
            raise web.seeother(login_url)

class live:
    def GET(self):
        if logged():
            return render.live(session.user)
        else:
            raise web.seeother(login_url)

class recommend:
    def GET(self):
        if logged():
            return render.recommend(session.user)
        else:
            raise web.seeother(login_url)

class logout:
    def GET(self):
        session.kill()
        raise web.seeother(login_url)

class listdata():
    def GET(self):
        pass

class appEdit():
    def POST(self):
        pass


class livePic():
    def __init__(self):
        self.start_tab = "live_splash"
        self.load_tab = "live_loading"

    def GET(self):
        data_type = web.input()
        what = "id, url, time, status, weight"

        if data_type.data == "starting":
            results = db.select(self.start_tab, what=what, order="status DESC, time DESC")
        elif data_type.data == "loading":
            results = db.select(self.load_tab, what=what, order="status DESC, time DESC")

        data = {}
        data["status"] = 200
        data["picData"] = []
        for r in results:
            item = {}
            item["id"] = r.id
            item["pic"] = STATIC + r.url
            item["time"] = r.time.strftime("%Y-%m-%d %H:%M:%S")
            if r.status == "1":
                item["state"] = True
            else:
                item["state"] = False
            item["weight"] = r.weight
            data["picData"].append(item)
        data = json.dumps(data)
        return data

    def POST(self):
        if logged():
            resp_data = {"status": 200}
            act = web.input().act
            input_data = json.loads(web.data())
            key = input_data["key"]
            data = json.loads(input_data["data"])

            if key == "starting":
                tab = self.start_tab
                pic_dir = START_PIC_DIR
            elif key == "loading":
                tab = self.load_tab
                pic_dir = LOAD_PIC_DIR

            if act == "update":
                self._update(tab, pic_dir, data)
            elif act == "add":
                self._add(tab, pic_dir, data)
            elif act == "delete":
                self._delete(tab, pic_dir, data)

            return json.dumps(resp_data)
        else:
            pass

    def _update(self, tab, pic_dir, data):
        url = data["pic"]
        id = data["id"]

        if "weight" in data:
            weight = data["weight"]
        else:
            weight = 1

        if "state" in data:
            if data["state"]:
                state = 1
            else:
                state = 0
        else:
            state = 1

        pic_name = os.path.basename(url)
        tmp_pic = "".join([sys.path[0], TMP_DIR, pic_name])
        url = "".join([pic_dir, pic_name])
        if os.path.exists(tmp_pic):
            # dst_dir = "".join([sys.path[0], pic_dir])
            dst_dir = "".join([sys.path[0], STATIC, pic_dir])
            shutil.copy(tmp_pic, dst_dir)

        where_vars = {"id": id}
        db.update(tab, vars=where_vars, where="id=$id", url=url, status=state, weight=weight)
        return True

    def _add(self, tab, pic_dir, data):
        url = data["pic"]
        if "weight" in data:
            weight = data["weight"]
        else:
            weight = 1

        pic_name = os.path.basename(url)
        tmp_pic = "".join([sys.path[0], url.replace(DOMAIN, "")])
        # dst_dir = "".join([sys.path[0], pic_dir])
        dst_dir = "".join([sys.path[0], STATIC, pic_dir])
        shutil.copy(tmp_pic, dst_dir)
        url = "".join([pic_dir, pic_name])
        ###########################
        db.insert(tab, url=url, status=0, weight=weight)
        ###########################
        return True

    def _delete(self, tab, pic_dir, data):
        id = data
        where_vars = {"id": id}
        results = db.select(tab, vars=where_vars, where="id=$id")
        url = results[0].url
        pic_name = os.path.basename(url)
        pic_path = "".join([sys.path[0], STATIC, pic_dir, "/", pic_name])
        os.rename(pic_path, "".join([pic_path, ".del"]))

        db.delete(tab, vars=where_vars, where="id=$id")



class livePicUpload:
    def POST(self):
        if logged():
            pic = web.input()
            dt = datetime.datetime.now()
            pic_suffix = os.path.splitext(pic.Filename)[-1]
            pic_name = "".join([dt.strftime("%Y%m%d-%H%M%S"), pic_suffix])
            pic_data = pic.Filedata
            tmp_pic = "".join([sys.path[0], TMP_DIR, pic_name])
            with open(tmp_pic, "w") as f:
                f.write(pic_data)

            data = {}
            data["status"] = 200
            data["url"] = "".join([DOMAIN, TMP_DIR, pic_name])
            data = json.dumps(data)
        else:
            resp_data = {"status": 500}
            data = json.dumps(resp_data)
            web.seeother(login_url)

        return data


if __name__ == "__main__":
    app.run()
