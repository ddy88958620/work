import live_probe as live


t = live.URLTranslater("http://v.qq.com/live/tv/46.html?pid=4172356212&flag=.moretv")
print t.realURL()