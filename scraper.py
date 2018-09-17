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
urls.extend([
	'https://pactwebserial.wordpress.com/2015/03/03/judgment-16-13/',
	'https://pactwebserial.wordpress.com/2015/03/07/epilogue/',
	'https://wildbow.wordpress.com/2015/03/07/pact-sealed/',
])

for i, url in enumerate(urls):
	if i == 52 and url == 'https://pactwebserial.wordpress.com/table-of-contents/':
		continue
	elif i == 130 and url == '4031384495743822299':
		url = 'https://pactwebserial.wordpress.com/2015/01/08/possession-15-2/'
	ch = url.rsplit('/', 2)[-2]
	name = '%03d-%s' % (i, ch)
	path = 'pact_raw/' + name
	if os.path.exists(path):
		print 'already have', name
		continue
	if url.startswith('pactwebserial.wordpress.com'):
		url = 'https://' + url
	print 'getting', name
	html = rs.get(url).content
	with open(path, 'w') as f:
		f.write(html)
