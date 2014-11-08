#!/usr/bin/env python

import os.path
import re

import requests

rs = requests.Session()
html = rs.get('https://pactwebserial.wordpress.com/table-of-contents/').content

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
	path = 'raw/%d' % i
	if os.path.exists(path):
		continue
	if i == 65 and url == 'https://pactwebserial.wordpress.com/2014/07/08/693/':
		url = 'https://pactwebserial.wordpress.com/2014/07/08/signature-8-1/'
	print 'getting', i, url
	if url.startswith('pactwebserial.wordpress.com'):
		url = 'https://' + url
	html = rs.get(url).content
	with open(path, 'w') as f:
		f.write(html)
