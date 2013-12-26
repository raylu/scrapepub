#!/usr/bin/env python

import requests

import re

start = 'http://www.talesofmu.com/book01/1' # 208.97.181.144
re_next = re.compile('<a href="(.*)" rel="next">')

rs = requests.Session()
url = start
while True:
	split = url.split('/')
	try:
		filename = int(split[-1])
	except ValueError:
		filename += 0.1
		if filename > 496.1:
			break
	print 'getting', filename
	html = rs.get(url).text
	with open('html/%s' % filename, 'w') as f:
		f.write(html.encode('utf-8'))

	match = re_next.search(html)
	url = match.group(1)
