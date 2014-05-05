
import httplib, httplib2, urllib, urllib2
import json, hashlib
import subprocess
import sys, os, re, time
import datetime
import random

from urlparse import urlparse


million = 1000 * 1000

eszie = 1024 * 1024 * 2	# byte
etime = 30 * 1000	# ms

block = 1024 * 200	# byte
first_data = 1024 * 4	# byte


class URLTranslater(object):
	def __init__(self, url):
		self.url = url

	def realURL(self):
		# print "call URLTranslater.realURL()...."
		realURL = ''
		domain = getOneReg(self.url, '''^.+?\.(\S+?)/.*''')
		# print "domain: %s" % domain

		if domain == 'eagleapp.tv':
			site = getOneReg(self.url, '''^.+?/url/(\w+)/.*''')
			print "site: %s" % site

			if site == 'letv':
				realURL = self.getLetvURL(self.url)
			elif site == 'sohu':
				realURL = self.getSohuURL(self.url)
			else:
				pass
		elif domain.find('letv.com') != -1:
			realURL = self.getLetvURL(self.url)
		elif domain.find('sohu.com') != -1:
			realURL = self.getSohuURL(self.url)
		elif domain.find('cntv.cn') != -1:
			realURL = self.getCntvURL(self.url)
		elif domain.find('pptv.com') != -1:
			realURL = self.getPPtvURL(self.url)
		elif domain.find('qq.com') != -1:
			if self.url.find('zb.v.qq.com') != -1:
				realURL = self.url
			else:
				realURL = self.getQQURL(self.url)
		else:
			realURL = self.url

		return realURL

	def getLetvURL(self, url):
		# print "call URLTranslater.getLetvURL()...."
		sid = getOneReg(url, '''^http://live.gslb.letv.com/gslb\?stream_id=(\w+)&tag=live''') or getOneReg(url, '''^http://parse.eagleapp.tv/url/letv/(\w+)$''')

		if sid:
			return self.getLetvURLbyStreamID(sid)
		else:
			return None

	def getLetvURLbyStreamID(self, sid):
		# print "call URLTranslater.getLetvURLbyStreamID()...."
		http = httplib2.Http(timeout=10)
		header = {"Accept": "application/json", 'Accept-Encoding': '*', 
						'User-Agent': 'AppleCoreMedia/1.0.0.9A405 (iPad; U; CPU OS 5_0_1 like Mac OS X; zh_cn)'}
		response, content = http.request('http://api.letv.com/time', 'GET', redirections=5, headers=header)
		jsn = json.loads(content)
		t = jsn['stime']

		white_list = ['shandong', 'anhui', 'shanxi', 'dongnan', 'hubei', 'yunnan', 'heilongjiang', 'guizhou', 'guangxi', 'henan', 'lvyou', 'dongfang', 'neimenggu', 'xinjiang', 'jilin', 'shanxi1', 'jiangxi', 'hebei', 'sichuan']
		tmp_id = sid
		if not sid in white_list:
			tmp_id = white_list[random.randint(1, len(white_list))] or 'dongfang'

		letv_str = "%s,%d,%s" % (tmp_id, t, '1ca1fc9546da2b196ce9edfa5decd787')
		key = md5sum(letv_str)

		play_url = "http://live.gslb.letv.com/gslb?tag=live&ext=m3u8&stream_id=%s&expect=3&termid=2&pay=0&ostype=macos&hwtype=ipad&sign=live_phone&format=1&platid=10&playid=1&splatid=1005&tm=%s&key=%s&_r=0" % (tmp_id, t, key)
		response, content = http.request(play_url, 'GET', redirections=5, headers=header)
		data = json.loads(content)
		l = data['location']
		p = re.compile('/m3u8/\w+')
		l = p.sub('/m3u8/' + sid, l)

		return l

	def getSohuURL(self, url):
		vid = getOneReg(url, '''^http://live.tv.sohu.com/(\w+)$''')
		if vid:
			t = time.time() / 1000000000
			jurl = 'http://live.tv.sohu.com/live/player_json.jhtml?encoding=utf-8&lid=%s&ver=21&type=1&g=8&t=%-10.10f' % (vid, t)
			http = httplib2.Http(timeout=10)
			print "%s" % jurl
			header = {"Accept": "*/*", 'Accept-Encoding': '*', 
						'User-Agent': 'AppleCoreMedia/1.0.0.9A405 (iPad; U; CPU OS 5_0_1 like Mac OS X; zh_cn)'}
			response, content = http.request(jurl, 'GET', redirections=5, headers=header)
			jsn = json.loads(content)
			return jsn['data']['hls'] + '&ext=m3u8'
		else:
			return url

	def getQQURL(self, url):
		u = getOneReg(url, '''^(.*)\?''')
		pid = getOneReg(url, '''.*\?pid=(\d+)''')

		uuu = urllib.quote(urllib.quote(u))

		jurl = 'http://zb.v.qq.com:1863/?rnd=428&txvjsv=2&ver=30103309&host=%s&apptype=live&pla=WIN&redirect=0&progid=%s' % (uuu, pid)
		http = httplib2.Http(timeout=10)
		header = {"Accept": "*/*", 'Accept-Encoding': '*', 
					'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.0 Safari/537.36'}
		response, content = http.request(jurl, 'GET', redirections=5, headers=header)
		play_url = getOneReg(content, '''url="(.*?)"''')
		return play_url

	def getCntvURL(self, url):
		code = getOneReg(url, '''live/(.*)''')
		_url = "http://vdn.live.cntv.cn/api2/liveHtml5.do?channel=pa://cctv_p2p_hd%s&client=html5" % code
		http = httplib2.Http(timeout=10)
		header = {"Accept": "*/*", 'Accept-Encoding': '*', 
					'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.0 Safari/537.36'}
		response, content = http.request(_url, 'GET', redirections=5, headers=header)
		jstr = getOneReg(content, 'var\s*html5VideoData\s*=\s*[\'\"]({.+})[\'\"]\s*;')
		data = json.loads(jstr)

		real_url = ''
		for (k, stream) in data['hls_url'].items():
			real_url = stream
			if stream.find('AUTH=') != -1:
				break

		return real_url

	def getPPtvURL(self, url):
		http = httplib2.Http(timeout=10)
		header = {"Accept": "*/*", 'Accept-Encoding': '*', 
					'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.0 Safari/537.36'}
		response, content = http.request(url, 'GET', redirections=5, headers=header)
		vid = getOneReg(content, '[\"\']id[\"\']\s*:\s*[\"\']?(\d+)[\"\']?')
		ctx = getOneReg(content, '[\"\']ctx[\"\']\s*:\s*[\"\'](.*?)[\"\']')
		kk = getOneReg(urllib.unquote(ctx), 'kk=(.*)$')

		real_url = 'http://web-play.pptv.com/web-m3u8-%s.m3u8?type=m3u8.web.pad&playback=0&kk=%s' % (vid, kk)
		print real_url
		return real_url


class httpLive(object):
	def __init__(self, url, opt):
		self.url = url
		self.opt = opt

		self.resp_time = 0

		self.redirect = 6
		self.output = open(opt, 'w')

	def probe(self, url):
		self.redirect -= 1
		startT = prevT = getTimeByUS()

		if url.find(".m3u8") != -1 or url.find("=m3u8") != -1 or url.find("-m3u8") != -1:
			print "switch to run hls live...."
			if self.output:
				self.output.close()
			hls = hlsLive()
			return hls.probe(url, self.opt)

		uri = urlparse(url)

		path = uri.path
		if uri.query != '':
			path += '?' + uri.query

		try:
			print uri.hostname, uri.port
			port = uri.port or 80
			header = {"Accept": "*/*", 'Accept-Encoding': '*', 
						'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.0 Safari/537.36'}
			httpClient = httplib.HTTPConnection(uri.hostname, port , timeout=10)
			httpClient.request('GET', path, headers=header)

			speedArr = []
			prevT = startT = getTimeByUS()
			resp_time = 0
			total = 0
			taken = 0

			response = httpClient.getresponse()

			print "get url: %s, status %d " % (url, response.status)
			if response.status >= 400:
				return False, None, None, None
			elif response.status >= 300 and response.status < 400:
				if self.redirect > 0:
					new_url = ""
					for header in response.getheaders():
						#print "%s: %s" % (header[0], header[1])
						if header[0] == "location" or header[0] == "refresh":
							new_url = header[1]

					if new_url != "":
						self.resp_time += getTimeByUS() - startT
						return self.probe(new_url)
					else:
						print "bad http response header!"
						return False
				else:
					print "too many redirect!"
					return False

			unit = 1024 * 4 	# 4 KB data of each reading
			first = True

			block_num = 0
			while (True):
				data = response.read(unit)

				if not data:
					return False, None, None, None

				if data and self.output:
					self.output.write(data)				

				size = len(data)
				taken += size
				total += len(data)

				if size <= 0:
					break

				if first and taken >= unit:
					first = False
					nowT = getTimeByUS()
					time_len = nowT - startT
					#print "startT: %d,    nowT: %d" % (startT, nowT)
					resp_time = time_len
					self.resp_time += resp_time

				if taken < block:
					continue

				block_num += 1

				nowT = getTimeByUS()
				time_len = nowT - prevT
				prevT = nowT

				if time_len > 0 and total:
					rate = (block * million) / (time_len * 1024.0)
					
					if block_num > 1:
						speedArr.append(rate)
						#print "avg speed of %d KB data:  %f KB/s" % (taken / 1024.0, rate)
					else:
						pass

				else:
					#print "invalid time: nowT=%d,  prevT=%d" % (nowT, prevT)
					pass

				if total >= eszie:
					break

				taken = 0

			#nowT = getTimeByUS()
			time_len = nowT - startT

			avg_speed = getAvgSpeed(total, time_len)
			jitter = getJitter(speedArr)

			resp_time = self.resp_time
			self.resp_time = 0

			if self.output:
				self.output.close()

			return True, avg_speed, jitter, resp_time

		except Exception, e:
			print e
		finally:
			if httpClient:
				httpClient.close()

class hlsLive(object):
	def __init__(self):

		self.resp_time = 0
		self.redirect = 6

		self.base = ''
		self.host = ''

		self.startT = getTimeByUS()

	def getM3u8(self, url):
	
		try:
			print "get m3u8 list, url: %s" % url
			http = httplib2.Http(timeout=10)
			header = {"Accept": "*/*", 'Accept-Encoding': '*', 
						'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.0 Safari/537.36'}
			response, content = http.request(url, 'GET', redirections=5, headers=header)			

			line = ''
			arr = []
			for i, ch in enumerate(content):
				line += ch

				if ch == '\r' or ch == '\n':
					if len(line) > 1:
						arr.append(line.strip())
						line = ''

			if len(line) > 1:
				arr.append(line.strip())
				line = ''

			#arr = content.split()

			count = 0
			new_url = ''

			if response['content-location'] != url:
				new_url = response['content-location']

			self.base = getOneReg(new_url, '''(http://\S+)/.*''')
			self.host = getOneReg(new_url, '''(http://\S+?)/.*''')
		
			# for l in arr:
			# 	print l

			ts_list = []
			while count < len(arr):
				line = arr[count]

				new_stream = ''

				if line.find('#EXT-X-STREAM-INF') != -1:
					target = arr[count + 1] 
					count += 1
					if target[0] == '/':
						new_stream = self.host + target
					elif target.find('http://') != -1:
						new_stream = target
					else:
						new_stream = self.base + '/' + target
				elif line.find('#EXTINF') != -1:
					target = arr[count + 1]
					count += 1

					ts_url = ''
					if target[0] == '/':
						ts_url = self.host + target
					elif target.find('http://') != -1:
						ts_url = target
					else:
						ts_url = self.base + '/' + target

					t = getOneReg(line, '''(\d+)''')
					item = {'ts': ts_url, 'time': t}
					#print item['ts'], item['time']
					ts_list.append(item)

				count = count + 1
				#print "new_stream: %s" % new_stream
				if new_stream != '':
					return self.getM3u8(new_stream)

			return ts_list

		except Exception, e:
			print e
			return []

	def probe(self, url, opt='tmp_ts'):

		try:
			ts_list = self.getM3u8(url)
			http = httplib2.Http(timeout=10)

			speedArr = []
			first = True

			total_size = 0
			total_time = 1

			sleepedT = 0.0

			if ts_list == []:
				return False

			print "start probing ts...."

			count = 0
			for item in ts_list:
				print item['ts'], item['time']
				count += 1

				sleepT = int(item['time'])
				startT = getTimeByUS()
				response, content = http.request(item['ts'], 'GET', redirections=5)
				size = len(content)
				endT = getTimeByUS()
				time_len = endT - startT
				rate = (size * million) / (time_len * 1024.0)

				print response.status
				if response.status >= 400:
					continue

				sleepT -= time_len / million
				if sleepT < 0:
					sleepT = 0

				print "avg speed of %d KB data:  %f KB/s" % (size / 1024.0, rate)

				if size > 0.0:
					speedArr.append(rate)

				total_size += size
				total_time += time_len

				#print "total_size: %d,    total_time: %d" % (total_size, total_time)
				if first:
					output = open(opt, 'w')
					output.write(content)
					output.close()

					first = False

				if count > 10:
					break

				sleepedT += sleepT
				time.sleep(sleepT)

			if len(speedArr) <= 0:
				return False

			avg_speed = getAvgSpeed(total_size, total_time)
			jitter = getJitter(speedArr)

			resp_time = getTimeByUS() - self.startT - total_time - sleepedT * million + 4 * million / avg_speed
			self.resp_time = 0

			return True, avg_speed, jitter, resp_time

		except Exception, e:
			print e
			return False, None, None, None


def dump(result):
	#print 'total size: %f KB, total time: %f ms' % result['total_size'], result['total_time']
	print 'avg speed: %f kB/s' % result['avg_speed']
	print 'Jitter: %f' % result['jitter']
	print "response_time: %f ms" % result['resp_time']

	print 'format: %s' % result['format']
	print 'bitrate: %s' % result['bitrate']
	print 'fps: %s' % result['fps']

def getOneReg(str, pattern):
	m = re.search(pattern, str)
	if m:
		return m.group(1)
	else:
		return None

def md5sum(text):
        m = hashlib.md5()
        m.update(text)
        return m.hexdigest()

def getTimeByUS():
	#now = datetime.datetime.now()
	now = time.time() * million
	return now

	
def getAvgSpeed(total, time_len):
	avg_speed = (total * million) / (time_len * 1024)
	return avg_speed


def getJitter(speedArr):
	n = 0
	sum = 0.0
	tmp_avg = 0.0
	variance2 = 0.0
	
	jitter = 0.0
	
	for speed in speedArr:
		n += 1
		sum += speed
		tmp_avg = sum / n
		variance2 += (speed - tmp_avg) ** 2
		#print(sum, tmp_avg, variance2)
		
	jitter = (variance2 / n) ** 0.5	
	return jitter

def external_cmd(cmd, msg_in=''):
    try:
        proc = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, 
        	stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout_value, stderr_value = proc.communicate(msg_in)
        return stdout_value, stderr_value
    except ValueError as err:
        return None, None
    except IOError as err:
        return None, None

def parse_result(result_str):
	avg_speed = getOneReg(result_str, '''avg_speed:\s*(\S+)\s*''')
	jitter = getOneReg(result_str, '''jitter:\s*(\S+)\s*''')
	resp_time = getOneReg(result_str, '''response_time:\s*(\S+)\s*''')
	total_time = getOneReg(result_str, '''total_time:\s*(\S+)\s*''')
	total_size = getOneReg(result_str, '''total_size:\s*(\S+)\s*''')

	if avg_speed and jitter and resp_time:
		return float(avg_speed), float(jitter), float(resp_time)
	else:
		return 0.0, 0.0, 0.0

def parse_ffmpeg_result(result_str):
	# print result_str
	format = getOneReg(result_str, '''Input\s*\#0,\s*(\w+),\s*from\s*''')
	bitrate = getOneReg(result_str, '''Duration:.*start:.*\s*bitrate:\s*(\d+)\s*''')
	fps = getOneReg(result_str, '''Video:.*?([\d\.]+)\s*tbr''')

	if format:
		return format, bitrate, fps
	else:
		return None, None, None

def parse_bitrate_result(result_str):
	bitrate = getOneReg(result_str, '''bitrate:\s*([\d\.]+)\s*Kbps''')

	return bitrate


def task(item):

	# print '##################################'
	# for k,v in item.items():
	# 	print k, '=>', v

	hostname, stderr_value = external_cmd('hostname')
	hostname = hostname.strip() or 'localhost'
	result = {'status': 0, 'hostname': hostname, 'url': item['url'], 'url_id': item['id'], 'avg_speed': 0.0, 'jitter': 0.0, 'resp_time': 0.0, 'bitrate': '', 'fps': '', 'format': ''}

	try:
		url_id = item['id']
		url_src = item['url']
		remark = item['remark']

		output = '/dev/shm/' + 'live_probe_tmp_file_%s' % time.strftime('%Y-%m-%d',time.localtime(time.time()))
		speed_str, stream_str = "", ""

		print "start live probing...."

		avg_speed, jitter, resp_time = 0.0, 0.0, 0

		urlTranslater = URLTranslater(url_src)
		url = urlTranslater.realURL()

		if url.find("rtmp://") != -1:
			print "run rtmp...."
			stdout_value, speed_str = external_cmd('rtest -r \'%s\' -o %s' % (url, output))
			#print "rtest output: %s" % stdout_value
			avg_speed, jitter, resp_time = parse_result(speed_str)

		elif url.find("rtsp://") != -1:
			print "run rtsp live...."
			return result
		elif url.find("http://") != -1:
			if url.find(".m3u8") != -1 or url.find("=m3u8") != -1 or url.find("-m3u8") != -1:
				print "run hls live...."
				hls = hlsLive()
				status, avg_speed, jitter, resp_time = hls.probe(url, output)

				if not status:
					return result
			else:
				print "run http live...."
				httpl = httpLive(url, output)
				status, avg_speed, jitter, resp_time = httpl.probe(httpl.url)
				
				if not status:
					return result
		else:
			print "unsupport protocol!"

		if avg_speed:
			result['avg_speed'] = avg_speed
			result['jitter'] = jitter
			result['resp_time'] = resp_time / 1000.0

		print "start running \"ffmpeg -i %s\"...." % output
		stdout_value, stream_str = external_cmd('ffmpeg -i %s' % output)
		format, bitrate, fps = parse_ffmpeg_result(stream_str)		

		if format:
			result['format'] = format			
			result['fps'] = fps

			if result['bitrate'] and result['bitrate'] != '':
				result['bitrate'] = bitrate
			else:
				stdout_value, stream_str = external_cmd('bitrater %s %s' % (output, fps))
				# print stdout_value, stream_str
				result['bitrate'] = parse_bitrate_result(stdout_value)
				print "video bitrate: %s" % result['bitrate']

		if status:
			result['status'] = '1'

		dump(result)
		print "\n"

		external_cmd('rm -f %s' % output)
		return result

	except Exception, e:
		print e
		return result

def main():
	print "start to run live prober...."
	item = {'id':1, 'url':sys.argv[1], 'remark':'test'}
	print task(item)


if __name__ == '__main__':
	main()