#!/usr/bin/env python

import errno
import os
import os.path
import sys

import requests
from bs4 import BeautifulSoup

books = {
	'arc01-12': (
		'https://www.parahumans.net/2017/10/21/glow-worm-0-1/',
		'https://www.parahumans.net/2019/03/29/heavens-12-x/'
	),
	'arc13-': (
		'https://www.parahumans.net/2019/04/02/black-13-1/',
		None
	),
}

book = sys.argv[1]
start, end = books[book]
dirname = 'worm2_%s_raw/' % book
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
		next_el = soup.find('a', string='Next Chapter')
	if next_el is None:
		next_el = soup.find('a', string=' Next Chapter')
	if next_el is None:
		if end is None:
			break
		raise Exception('could not find next')
	url = next_el['href']
	i += 1
