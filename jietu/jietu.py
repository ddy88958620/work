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

tmp_path = sys.path[0] + "/tmp/"
# 整个脚本运行完成后将tmp中所有截图移动到snapshot文件夹中
snapshot_path = sys.path[0] + "/snapshot/"

ffm_cmd ="./ffmpeg -i %s -f image2 -ss 1 -s 250x180 -vframes 1 %s -y"

# 仅作为运行时计数用
COUNT = 0
count_lock = threading.Lock()
# 截屏超时
snap_timeout = 10

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
    # 通过解析获取真实的Url
    cntv_url = search("cntv_flv", src_list)
    qq_url = search("qq", src_list)
    sohu_url = search("sohu", src_list)
    ysten_url = search("ysten", src_list)
    other_url = src_list[0]["url"]
    try:
        if cntv_url:
            return cntv_url
        elif qq_url:
            real_url = live_probe.URLTranslater(qq_url).realURL()
            return real_url
        elif ysten_url:
            real_url = live_probe.URLTranslater(ysten_url).realURL()
            return real_url
        elif sohu_url:
            real_url = live_probe.URLTranslater(sohu_url).realURL()
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
    # ffmpeg截图命令第一个参数为url，第二个参数为截图文件名
    cmd = ffm_cmd % (url, pic_name)
    cmd_list = cmd.split(" ")
    p = subprocess.Popen(cmd_list, stderr=subprocess.PIPE)

    # 每秒检查一次ffmpeg截图进程是否完成，若8秒仍未完成杀死此进程
    for timer in range(snap_timeout):
        try:
            ret = p.poll()
            if ret:
                p.terminate()
                break
            elif (ret == None and timer == snap_timeout - 1):
                p.terminate()
                return False
            time.sleep(1)
        except:
            return False

    return True


# 打印完成信息
def printFinish(code):
    global COUNT
    count_lock.acquire()
    COUNT += 1
    print "\033[1;32;40m------>", COUNT, code, "finished.\033[0m"
    count_lock.release()


# 检查截图是否成功，若不成功遍历整个url列表直至截图成功
def snapshot(code, src_list):
    global COUNT
    url = selectBestUrl(code, src_list)
    pname = code + ".jpg"
    snap(url, pname)
    # 如果最佳url截图不成功
    time.sleep(2)
    if not os.path.exists(tmp_path+pname):
        print code, "------> first try failed! ------>", url
        success = False
        for src in src_list:
            try:
                url = live_probe.URLTranslater(src["url"]).realURL()
                # print "------> try", url
                snap(url, pname)
                time.sleep(2)
                if not os.path.exists(tmp_path+pname):
                    continue
                else:
                    success = True
                    printFinish(code)
                    break
            except Exception, e:
                print e
                continue

        if not success:
            print "\033[1;31;40m------>", pname, "can not be created!\033[0m"
    else:
        printFinish(code)


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
                if not src_list:
                    print "\033[1;31;40m------>", code, "src_list is None!\033[0m"
                else:
                    snapshot(code, src_list)
                self.queue.task_done()
            else:
                break


def main():
    start = time.time()
    subprocess.Popen("rm "+tmp_path+"*", shell=True)

    code_list = getCodes()
    for code in code_list:
        queue.put(code)

    for i in range(10):
        t = SnapThread(queue)
        t.setDaemon(True)
        t.start()

    queue.join()

    subprocess.Popen("mv "+tmp_path+"* "+snapshot_path, shell=True)

    print time.time() - start, "s"

if __name__ == "__main__":
    main()
