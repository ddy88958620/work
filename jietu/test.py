import subprocess
import sys
import live_probe

cmd = "./ffmpeg -i %s -f image2 -ss 1 -s 250x180 -vframes 1 test.jpg -y"
url = live_probe.URLTranslater(sys.argv[1]).realURL()
print "****", url, "\n\n"
cmd = cmd % url
cmd_list = cmd.split(" ")
p = subprocess.Popen(cmd_list)