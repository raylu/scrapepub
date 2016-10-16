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
		'https://tiraas.wordpress.com/2014/08/20/book-1-prologue/',
		'https://tiraas.wordpress.com/2015/02/13/epilogue-vol-1/'
	),
	'vol2': (
		'https://tiraas.wordpress.com/2015/02/24/volume-2-prologue/',
		'https://tiraas.wordpress.com/2015/08/28/epilogue-volume-2/'
	),
	'vol3': (
		'https://tiraas.wordpress.com/2015/09/14/prologue-volume-3/',
		'https://tiraas.wordpress.com/2016/07/15/epilogue-volume-3/'
	),
	'vol4': (
		'https://tiraas.wordpress.com/2016/07/29/prologue-volume-4/',
		None
	),
}
start, end = bounds[vol]
dirname = 'gab_%s_raw/' % vol
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
		if end is None:
			break
		raise Exception('could not find next')
	else:
		url = next_el['href']
	i += 1
