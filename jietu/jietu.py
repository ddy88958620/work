#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import subprocess
import time
import utils
import os
import Queue
import threading
import live_probe


<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> fcb98426123fb48a11c98028531885746774c98b
# 获取url源优先顺序(site列表)
prior_list = ["ppu.17kds.net", "jsitv", "qq", "sohu", "ysten"]
# 排除的排除可能有问题的源的列表
except_list = ["cntv", "cntv_hls", "letv", "letv_mtv"]
<<<<<<< HEAD
=======
# 获取url源优先顺序
prior_list = ["cntv.wscdns", "qq", "sohu", "ysten"]
# 排除可能有问题的源的列表
except_list = ["cntv", "cntv_hls"]
>>>>>>> 85a34183b10450e8e9479f801435fe4a3e95566e
=======
>>>>>>> fcb98426123fb48a11c98028531885746774c98b
# 暂存文件路径
tmp_path = "".join([sys.path[0], "/tmp/"])
# 整个脚本运行完成后将tmp中所有截图移动到snapshot文件夹中
snapshot_path = "".join([sys.path[0], "/snapshot/"])
# log文件路径
<<<<<<< HEAD
log_path = "".join([sys.path[0], "/log.txt"])
# log文件读取锁
log_lock = threading.Lock()
=======
log_path = "".join([sys.path[0], "/log.json"])
>>>>>>> fcb98426123fb48a11c98028531885746774c98b
# ffmpeg截图命令
ffm_cmd = "".join([sys.path[0], "/ffmpeg -i %s -f image2 -ss 1 -s 250x180 -vframes 1 %s -y"])
# 仅作为运行时计数用
COUNT = 0
count_lock = threading.Lock()
# 截屏超时
snap_timeout = 15
# code队列
queue = Queue.Queue()

pid_list = []

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


# 按照prior列表对src_list进行排序
def sortSrcs(src_list):
    sorted_srcs = []
    for site in prior_list:
        for src in src_list:
            if src["site"] == site:
                sorted_srcs.append(src)

<<<<<<< HEAD
<<<<<<< HEAD
=======
    # for src in src_list:
    #     if src["site"] not in prior_list or src["site"] not in except_list:

>>>>>>> 85a34183b10450e8e9479f801435fe4a3e95566e
=======
>>>>>>> fcb98426123fb48a11c98028531885746774c98b
    other_srcs = [x for x in src_list if x["site"] not in sorted_srcs and x["site"] not in except_list]
    sorted_srcs.extend(other_srcs)
    return sorted_srcs


# 根据url截图
def snap(url, pname):
    if not url:
        return False

    pic_name = "".join([tmp_path, pname])
    # ffmpeg截图命令第一个参数为url，第二个参数为截图文件名
    cmd = ffm_cmd % (url, pic_name)
    cmd_list = cmd.split(" ")
    p = subprocess.Popen(cmd_list, stderr=subprocess.PIPE)
    pid_list.append(p.pid)

    # 每秒检查一次ffmpeg截图进程是否完成，若timout到了仍未完成杀死此进程
    for timer in range(snap_timeout):
        try:
            ret = p.poll()
            if ret:
                time.sleep(2)
                p.terminate()
                return True
            elif timer == snap_timeout - 1:
                p.terminate()
                return False
            time.sleep(1)
        except:
            return False


# 打印完成信息
def printFinish(code):
    global COUNT
    count_lock.acquire()
    COUNT += 1
    print "\033[1;32;40m------>", COUNT, code, "finished.\033[0m"
    count_lock.release()


# 遍历整个src_list并截图，并返回结果信息
def snapshot(code, src_list):
    logger = utils.Logger(code, log_path)

    if not src_list:
        # log_lock.acquire()
        print "\033[1;31;40m------> src_list of", code, "is empty!\033[0m"
        logger.log(level=3)
        # log_lock.release()
        return False

    global COUNT
    pname = "".join([code, ".jpg"])
    sorted_srcs = sortSrcs(src_list)

    for src in sorted_srcs:
        try:
            url = live_probe.URLTranslater(src["url"]).realURL()
            snap(url, pname)
            if os.path.exists("".join([tmp_path, pname])):
                printFinish(code)
<<<<<<< HEAD
<<<<<<< HEAD
                logger.log(1, url)
=======
                with open("problem.txt", "a+") as f:
                    f.write(code + ": " + url + "\n")
>>>>>>> 85a34183b10450e8e9479f801435fe4a3e95566e
=======
                logger.log(1, url)
>>>>>>> fcb98426123fb48a11c98028531885746774c98b
                return True
            else:
                logger.log(2, url)
        except Exception, e:
            print e

    logger.log(level=3)
    print "\033[1;31;40m------>", pname, "can not be created!\033[0m"
    return False


# 多线程截图类
class SnapThread(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        global COUNT
        while True:
            if not self.queue.empty():
                code = self.queue.get()
                print "snapshoting", code
                src_list = getSrcList(code)
                snapshot(code, src_list)
                self.queue.task_done()
            else:
                break

def init():
    if not os.path.exists(tmp_path):
        os.makedirs(tmp_path)

    if not os.path.exists(snapshot_path):
        os.makedirs(snapshot_path)

    with open(log_path, "w+") as f:
	   pass
       
    subprocess.call("".join(["rm ", tmp_path, "*"]), stderr=subprocess.PIPE, shell=True)


def main():
    start = time.time()

    init()

    if len(sys.argv) > 1:
        code_list = [sys.argv[1]]
    else:
        code_list = getCodes()

    for code in code_list:
        queue.put(code)

    for i in range(10):
        t = SnapThread(queue)
        t.setDaemon(True)
        t.start()

    queue.join()

    subprocess.call("".join(["mv ", tmp_path, "* ", snapshot_path]), shell=True)

    for pid in pid_list:
        subprocess.call("".join(["kill -9 ", str(pid)]), stderr=subprocess.PIPE, shell=True)

    print time.time() - start, "s"

if __name__ == "__main__":
    main()
