#!/usr/bin/env python

import requests

import os
import re
import sys

meta = { # 208.97.181.144
	'vol1': ('http://www.talesofmu.com/book01/1', 496.1),
	'vol2': ('http://www.talesofmu.com/volume-2/chapter-1', 338),
}
start, end = meta[sys.argv[1]] # 208.97.181.144
re_next = re.compile('<a href="(.*)" rel="next">')

rs = requests.Session()
url = start
while True:
	filename_str = url.split('/')[-1]
	if filename_str.startswith('chapter-'):
		filename_str = filename_str[8:]
	try:
		filename = int(filename_str)
	except ValueError:
		split = str(filename).split('.')
		ipart = split[0]
		try:
			fpart = int(split[1])
		except IndexError:
			fpart = 0
		filename = '%s.%d' % (ipart, fpart + 1)
	path = 'tomu_%s_raw/%s' % (sys.argv[1], filename)
	if os.path.exists(path):
		print 'skipping', filename
		with open(path, 'r') as f:
			html = f.read()
	else:
		print 'getting', filename
		html = rs.get(url).text
		with open(path, 'w') as f:
			f.write(html.encode('utf-8'))

	if filename == end:
		break
	match = re_next.search(html)
	url = match.group(1)
