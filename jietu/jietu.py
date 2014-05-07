#-*- coding: utf-8 -*-

import subprocess
import time
import sys
import utils
import os
import Queue
import threading
import live_probe

reload(sys)
sys.setdefaultencoding('utf8')

# 每次脚本获取的截图暂存在tmp文件夹中以便截图过程中检查截图是否成功并采取对策应对
tmp_path = "./tmp/"
# 整个脚本运行完成后将tmp中所有截图移动到snapshot文件夹中
snapshot_path = "./snapshot/"
# ffmpeg截图命令第一个参数为url，第二个参数为截图文件名
ffm_cmd = "./ffmpeg -i '%s' -f image2 -ss 1 -s '250x180' -vframes 1 '%s' -y"

queue = Queue.Queue()

# 从数据库中获取需要截图的频道code列表
def getCodes():
    query = "SELECT code FROM mtv_channel WHERE `snapshot` = 1"
    s = utils.Sql()
    codes = s.select(query)
    code_list = []
    for c in codes:
        code_list.append(c[0])
    return code_list

# 根据频道code从库中获取该频道下所有url
def getSrcList(code):
    query = "SELECT site, url FROM mtv_source WHERE code = %s and status = 1"
    params = (code, )
    s = utils.Sql()
    srcs = s.select(query, params=params)
    src_list = []
    for u in srcs:
        src = {}
        src["site"] = u[0]
        src["url"] = u[1]
        src_list.append(src)
    return src_list

# 查找一个url列表中是否有对应来源的url
def search(key, src_list):
    for src in src_list:
        if key in src["site"]:
            return src["url"]
    else:
        return False

# 从url列表中选择可能的最优截图url
def selectBestUrl(code, src_list):
    try:
        # 央视以cntv源为最优
        if "cctv" in code:
            url = search("cntv_flv", src_list)
            if url:
                return url
            else:
                url = src_list[0]["url"]
                live = live_probe.URLTranslater(url)
                real_url = live.realURL()
                return real_url
        else:
            # 卫视频道优先顺序为qq, 搜狐, 易视腾, 其他
            qq_url = search("qq", src_list)
            sohu_url = search("sohu", src_list)
            ysten_url = search("ysten", src_list)
            other_url = src_list[0]["url"]

            # 通过解析获取真实的Url
            if qq_url:
                real_url = live_probe.URLTranslater(qq_url).realURL()
                return real_url
            elif sohu_url:
                real_url = live_probe.URLTranslater(sohu_url).realURL()
                return real_url
            elif ysten_url:
                real_url = live_probe.URLTranslater(ysten_url).realURL()
                return real_url
            else:
                real_url = live_probe.URLTranslater(other_url).realURL()
                return real_url
    except Exception, e:
        print e
        return src_list[0]

# 根据url截图
def snap(url, pname):
    pic_name = tmp_path + pname
    cmd = ffm_cmd % (url, pic_name)
    out = subprocess.Popen(cmd, stderr=subprocess.PIPE, shell=True)
    # 每秒检查一次ffmpeg截图进程是否完成，若10秒仍未完成杀死此进程
    for timer in range(10):
        ret = out.poll()
        if ret:
            return True
        elif ret == None and timer == 9:
            out.kill()
            return False

        time.sleep(1)

# 检查截图是否成功，若不成功遍历整个url列表直至截图成功
def snapshot(code, src_list):
    url = selectBestUrl(code, src_list)
    pname = code + ".jpg"
    snap(url, pname)
    # 如果最佳url截图不成功
    if not os.path.exists(tmp_path+pname):
        print code, "------> first try failed!"
        success = False
        for src in src_list:
            try:
                url = live_probe.URLTranslater(src["url"]).realURL()
                print "------> try", url
                snap(url, pname)
                if not os.path.exists(tmp_path+pname):
                    continue
                else:
                    success = True
                    break
            except Exception, e:
                print e
                continue

        if not success:
            print "------>", pname, "can not be created!"

    print "\033[1;32;40m------>", SnapThread.count+1, code, "finished. \033[0m"

# 多线程截图类
class SnapThread(threading.Thread):
    count = 0
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            if not self.queue.empty():
                code = self.queue.get()
                print "snapshoting", code
                src_list = getSrcList(code)
                if not src_list:
                    print"------>", code, "src_list is None!"
                else:
                    snapshot(code, src_list)
                self.queue.task_done()
                SnapThread.count += 1
            else:
                break

# 将tmp文件中截图移至snapshot文件夹
def movePic():
    cmd = "mv " + tmp_path + "* " + snapshot_path
    subprocess.Popen(cmd, shell=True)


def main():
    start = time.time()
    # 每次脚本运行前清空tmp文件夹
    cmd = "rm "+tmp_path+"*"
    subprocess.Popen(cmd, shell=True)
    code_list = getCodes()

    for code in code_list:
        queue.put(code)

    for i in range(10):
        t = SnapThread(queue)
        # t.setDaemon(True)
        t.start()

    # queue.join()
    while True:
        if SnapThread.count == len(code_list):
            break
        else:
            time.sleep(1)
    movePic()
    print time.time() - start, "s"

if __name__ == "__main__":
    main()
