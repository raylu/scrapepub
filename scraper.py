#!/usr/bin/env python

import os
import sys

import requests
from bs4 import BeautifulSoup

book = sys.argv[1]
bounds = {
	'book1': (
		'https://practicalguidetoevil.wordpress.com/2015/03/25/prologue/',
		'https://practicalguidetoevil.wordpress.com/2015/11/04/prologue-2/'
	),
	'book2': (
		'https://practicalguidetoevil.wordpress.com/2015/11/04/prologue-2/',
		'https://practicalguidetoevil.wordpress.com/2016/10/12/heroic-interlude-prise-au-fer/'
	),
}
start, end = bounds[book]
dirname = 'pgte_%s_raw/' % book
os.mkdir(dirname)

rs = requests.Session()
url = start
i = 0
while url != end:
	name = url.rsplit('/', 2)[1]
	filename = '%02d-%s' % (i, name)
	print 'getting', filename
	content = rs.get(url).content
	with open(dirname + filename, 'w') as f:
		f.write(content)
	soup = BeautifulSoup(content, 'lxml')
	next_el = soup.find('link', rel='next')
	url = next_el['href']
	i += 1
