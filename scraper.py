#!/usr/bin/env python

import re

import requests

rs = requests.Session()
html = rs.get('http://parahumans.wordpress.com/table-of-contents/').content

split = html.split('\n')
urls = []
started = False
for line in split:
	if started:
		if 'id="jp-post-flair"' in line:
			break
		match = re.search('href="(.*?)"', line)
		if match:
			urls.append(match.group(1))
	elif 'class="entry-content"' in line:
		started = True

for i, url in enumerate(urls):
	print 'getting', i, url
	html = rs.get(url).content
	with open('raw/%d' % i, 'w') as f:
		f.write(html)
