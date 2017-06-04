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
		'http://www.starwalkerblog.com/startup-sequence/',
		'http://www.starwalkerblog.com/sneak-peek-keida/'
	),
	'book2': (
		'http://www.starwalkerblog.com/more-than/',
		'http://www.starwalkerblog.com/authors-note-book-2-complete/'
	),
	'book3': (
		'http://www.starwalkerblog.com/the-loyalty-of-pawns/',
		'http://www.starwalkerblog.com/authors-note-book-3-and-a-hiatus/'
	),
	'book4': (
		'http://www.starwalkerblog.com/sarabande-station/',
		None
	),
}
start, end = bounds[book]
dirname = 'starwalker_%s_raw/' % book
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
