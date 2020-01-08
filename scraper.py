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
		'https://wanderinginn.wordpress.com/2017/07/29/2-41/',
	),
	'vol3': (
		'https://wanderinginn.wordpress.com/2017/08/01/3-00-e/',
		'https://wanderinginn.wordpress.com/2017/12/30/interlude-4/',
	),
	'vol4': (
		'https://wanderinginn.wordpress.com/2018/01/06/4-00-k/',
		'https://wanderinginn.com/2018/07/09/the-depthless-doctor/',
	),
	'vol5': (
		'https://wanderinginn.com/2018/10/19/glossary/',
		'https://wanderinginn.com/2019/03/02/interlude-5/',
	),
	'vol6': (
		'https://wanderinginn.com/2019/03/19/6-00/',
		None,
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
	elif url == 'https://wanderinginn.com/2018/10/19/glossary/':
		url = 'https://wanderinginn.com/2018/07/10/5-00/'
	elif url == 'https://wanderinginn.com/2018/10/16/5-29/':
		url = 'https://wanderinginn.com/2018/10/20/5-30-g/'
	else:
		soup = BeautifulSoup(content, 'lxml')
		next_el = soup.find('link', rel='next')
		if next_el is None:
			if end is None:
				break
			raise Exception('could not find next')
		url = next_el['href']
	i += 1
