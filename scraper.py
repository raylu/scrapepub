#!/usr/bin/env python

import requests

import os
import re
import sys

start = 'https://twigserial.wordpress.com/2014/12/24/taken-roots-1-1/'
end = 'https://twigserial.wordpress.com/2015/08/25/esprit-de-corpse-5-12/'
re_next = re.compile("<link rel='next' title='.*' href='(.*)' />")

rs = requests.Session()
url = start
i = 1
while True:
	filename = url.rsplit('/', 2)[-2]
	path = 'twig_raw/%d.%s' % (i, filename)
	if os.path.exists(path):
		print 'skipping', filename
		with open(path, 'r') as f:
			html = f.read()
	else:
		print 'getting', filename
		html = rs.get(url).text
		with open(path, 'w') as f:
			f.write(html.encode('utf-8'))

	if url == end:
		break
	match = re_next.search(html)
	url = match.group(1)
	i += 1
