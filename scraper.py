#!/usr/bin/env python

import errno
import os
import os.path
import sys

import requests
from bs4 import BeautifulSoup

book = sys.argv[1]
bounds = {
	'book1': (
		'https://tiraas.wordpress.com/2014/08/20/book-1-prologue/',
		'https://tiraas.wordpress.com/2014/10/08/1-21/'
	),
	'book2': (
		'https://tiraas.wordpress.com/2014/10/10/2-1/',
		'https://tiraas.wordpress.com/2014/11/28/2-22/',
	),
}
start, end = bounds[book]
dirname = 'gab_%s_raw/' % book
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
	filename = '%02d-%s' % (i, name)
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
		url = None
	else:
		url = next_el['href']
	i += 1
