#!/usr/bin/env python2

import errno
import os
import os.path
import sys

import requests
from bs4 import BeautifulSoup

book = sys.argv[1]
bounds = {
	'book1': (
		'https://palelights.com/2022/08/17/chapter-1/',
		None,
	),
}
start, end = bounds[book]
dirname = 'palelights_%s_raw/' % book
try:
	os.mkdir(dirname)
except OSError as e:
	if e.errno != errno.EEXIST:
		raise

rs = requests.Session()
rs.headers['User-Agent'] = 'Mozilla/5.0'
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
	else:
		soup = BeautifulSoup(content, 'lxml')
		next_el = soup.find('link', rel='next')
		if next_el is None:
			next_el = soup.find('a', rel='next')
			if next_el is None:
				if end is None:
					break
				raise Exception('could not find next')
		url = next_el['href']
	i += 1
