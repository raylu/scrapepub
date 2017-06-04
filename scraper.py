#!/usr/bin/env python

import errno
import os
import os.path
import sys

import requests
from bs4 import BeautifulSoup

vol = sys.argv[1]
bounds = {
	'vol1': (
		'https://wanderinginn.wordpress.com/2016/07/27/1-00/',
		'https://wanderinginn.wordpress.com/2017/03/04/1-45/'
	),
	'vol2': (
		'https://wanderinginn.wordpress.com/2017/03/07/interlude-2/',
		None
	),
}
start, end = bounds[vol]
dirname = 'inn_%s_raw/' % vol
try:
	os.mkdir(dirname)
except OSError as e:
	if e.errno != errno.EEXIST:
		raise

rs = requests.Session()
url = start
i = 0
while True:
	name = url.rsplit('/', 2)[1]
	filename = '%03d-%s' % (i, name)
	if os.path.exists(dirname + filename):
		print 'already have', filename
		with open(dirname + filename, 'r') as f:
			content = f.read()
	else:
		print 'getting', filename
		content = rs.get(url).content
		with open(dirname + filename, 'w') as f:
			f.write(content)
	if url == end:
		break
	soup = BeautifulSoup(content, 'lxml')
	next_el = soup.find('link', rel='next')
	if next_el is None:
		if end is None:
			break
		raise Exception('could not find next')
	url = next_el['href']
	i += 1
