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


LOAD_PIC_DIR = "/image/loading/"
START_PIC_DIR = "/image/splash/"
STATIC = "/static"
TMP_DIR = "/static/tmp/"
# DOMAIN = "http://eagleapp.tv:57709"
DOMAIN = "http://210.73.218.156:57709"
render = web.template.render("templates/")

urls = (
    "/login.html", "login",
    "/index.html", "index",
    "/picture.html", "picture",
    "/live.html", "live",
    "/recommend.html", "recommend",

    # 接口
    "/logout", "logout",                    # 登出
    "/live_pic", "livePic",                 # 直播配图
    "/live_pic_upload", "livePicUpload",    # 直播配图上传
    "/live_classify", "liveClassify",       # 直播分类
    "/live_source", "liveSource",            # 直播源列表
    "/listdata", "listdata",                # 应用列表
    "/app_edit", "appEdit",
    "/app_delete", "appDelete",
    "/app_classify", "appClassify",
    "/recommend_edit", "recommendEdit",
    "/recommend_delete", "recommendDelete",
    "/recommend_build", "recommendBuild",
    "/live_edit", "liveEdit",
    "/live_delete", "liveDelete",
    "/live_build", "liveBuild",
    "/upload_test", "uploadTest",
    "/test", "Test",
)

login_url = "/login.html"
index_url = "/index.html"

app = web.application(urls, globals())
db = web.database(dbn="mysql", db=config.db,
                  user=config.user, pw=config.passwd)

# web.config.debug = False
# initializer = {
#     "loggedin": False,
#     "user": None
# }
# session = web.session.Session(
#     app, web.session.DiskStore("sessions"), initializer=initializer)
# web.config.session_parameters['cookie_name'] = 'session_id'
# web.config.session_parameters["timeout"] = 300
# web.config.session_parameters["ignore_expiry"] = False
# web.config.session_parameters["ignore_change_ip"] = False
# web.config.session_parameters['expired_message'] = "Session expired"


if web.config.get('_session') is None:
    initializer = {
        "loggedin": False,
        "user": None
    }
    session = web.session.Session(
        app, web.session.DiskStore("sessions"), initializer=initializer)
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
    pw_hash = hashlib.md5(pw).hexdigest()
    sault_hash = hashlib.md5(user).hexdigest()
    saulted = hashlib.md5("".join([pw_hash, sault_hash])).hexdigest()
    user_vars = {"user": user, "pw": saulted}
    exist = db.select("admins", vars=user_vars,
                      where="uname=$user and passwd=$pw")
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


class liveSource:

    def GET(self):
        if not logged():
            return json.dumps({"status": 403})

        data = web.input()
        web.debug(data)
        tag_vars = {"code": data.code}
        tid = db.select("live_tag", vars=tag_vars, where="code=$code")[0].id
        ch_vars = {"tagid": tid}
        ch_results = db.select(
            "live_channel", vars=ch_vars, where="tagid=$tagid")
        ch_list = []
        for ch in ch_results:
            channel = {}
            channel["chid"] = ch.id
            channel["name"] = ch.name
            channel["state"] = ch.state
            channel["types"] = data.code
            src_vars = {"chid": ch.id}
            src_results = db.select(
                "live_source", vars=src_vars, where="chid=$chid")
            channel["list"] = []
            for s in src_results:
                src = {}
                src["srcid"] = s.id
                src["source"] = s.source
                src["playUrl"] = s.url
                src["state"] = s.state
                channel["list"].append(src)

            ch_list.append(channel)

        resp_data = {"status": 200, "liveData": ch_list}
        return json.dumps(resp_data)


class liveClassify:

    def GET(self):
        if not logged():
            return json.dumps({"status": 403})
        results = db.select("live_tag")
        tag_list = []
        for r in results:
            tag = {}
            tag["name"] = r.tagname
            tag["code"] = r.code
            tag_list.append(tag)

        resp_data = {"status": 200, "classifyLiveData": tag_list}

        return json.dumps(resp_data)

    def POST(self):
        if not logged():
            return json.dumps({"status": 403})

        act = web.input().act
        data = json.loads(web.data())

        if act == "add":
            self._add(data)
        elif act == "update":
            self._update(data)
        elif act == "delete":
            self._delete(data)
        elif act == "build":
            self._build(data)

    def _add(self, data):
        pass

    def _update(self, data):
        pass

    def _delete(self, data):
        pass

    def _build(self, data):
        pass


class livePic():

    def __init__(self):
        self.start_tab = "live_splash"
        self.load_tab = "live_loading"

    def GET(self):
        if not logged():
            return json.dumps({"status": 403})

        data_type = web.input()
        what = "id, url, time, status, weight"

        if data_type.data == "starting":
            results = db.select(self.start_tab, what=what,
                                order="status DESC, time DESC")
        elif data_type.data == "loading":
            results = db.select(self.load_tab, what=what,
                                order="status DESC, time DESC")

        resp_data = {"status": 200, "picData": []}
        for r in results:
            item = {}
            item["id"] = r.id
            item["pic"] = "".join([STATIC, r.url])
            item["time"] = r.time.strftime("%Y-%m-%d %H:%M:%S")
            item["weight"] = r.weight
            if r.status == "1":
                item["state"] = True
            else:
                item["state"] = False
            resp_data["picData"].append(item)
        return json.dumps(resp_data)

    def POST(self):
        if not logged():
            return json.dumps({"status": 403})

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

        resp_data = {"status": 200}
        if act == "update":
            self._update(tab, pic_dir, data)
        elif act == "add":
            pic_data = self._add(tab, pic_dir, data)
            resp_data["picData"] = pic_data
        elif act == "delete":
            self._delete(tab, pic_dir, data)

        return json.dumps(resp_data)

    def _update(self, tab, pic_dir, data):
        url = data["pic"]
        id = data["id"]

        if "weight" in data:
            weight = data["weight"]
        else:
            weight = 1

        if "state" in data:
            if data["state"]:
                state = "1"
            else:
                state = "0"
        else:
            state = "1"

        pic_name = os.path.basename(url)
        tmp_pic = "".join([sys.path[0], TMP_DIR, pic_name])
        url = "".join([pic_dir, pic_name])
        if os.path.exists(tmp_pic):
            # dst_dir = "".join([sys.path[0], pic_dir])
            dst_dir = "".join([sys.path[0], STATIC, pic_dir])
            shutil.copy(tmp_pic, dst_dir)

        where_vars = {"id": id}
        t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db.update(tab, vars=where_vars, where="id=$id",
                  url=url, status=state, weight=weight, time=t)
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
        t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        id = db.insert(tab, url=url, status=0, time=t, weight=weight)

        pic_data = {}
        pic_data["id"] = id
        pic_data["pic"] = "".join([STATIC, url])
        pic_data["weight"] = weight
        pic_data["time"] = t
        pic_data["state"] = False

        return pic_data

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
        if not logged():
            return json.dumps({"status": 403})

        pic = web.input()
        dt = datetime.datetime.now()
        pic_suffix = os.path.splitext(pic.Filename)[-1]
        pic_name = "".join([dt.strftime("%Y%m%d-%H%M%S"), pic_suffix])
        pic_data = pic.Filedata
        tmp_pic = "".join([sys.path[0], TMP_DIR, pic_name])
        with open(tmp_pic, "w") as f:
            f.write(pic_data)

        resp_data = {"status": 200, "url": "".join([DOMAIN, TMP_DIR, pic_name])}
        return json.dumps(resp_data)


if __name__ == "__main__":
    app.run()
