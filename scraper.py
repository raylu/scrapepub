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
		'https://practicalguidetoevil.wordpress.com/2015/03/25/prologue/',
		'https://practicalguidetoevil.wordpress.com/2015/11/04/prologue-2/',
	),
	'book2': (
		'https://practicalguidetoevil.wordpress.com/2015/11/04/prologue-2/',
		'https://practicalguidetoevil.wordpress.com/2017/02/08/prologue-3/',
	),
	'book3': (
		'https://practicalguidetoevil.wordpress.com/2017/02/08/prologue-3/',
		'https://practicalguidetoevil.wordpress.com/2018/04/09/prologue-4/',
	),
	'book4': (
		'https://practicalguidetoevil.wordpress.com/2018/04/09/prologue-4/',
		'https://practicalguidetoevil.wordpress.com/2019/01/14/prologue-5/',
	),
	'book5': (
		'https://practicalguidetoevil.wordpress.com/2019/01/14/prologue-5/',
		'https://practicalguidetoevil.wordpress.com/2020/01/06/prologue-6/',
	),
	'book6': (
		'https://practicalguidetoevil.wordpress.com/2020/01/06/prologue-6/',
		'https://practicalguidetoevil.wordpress.com/2021/03/02/prologue-7/',
	),
	'book7': (
		'https://practicalguidetoevil.wordpress.com/2021/03/02/prologue-7/',
		None,
	),
}
start, end = bounds[book]
dirname = 'pgte_%s_raw/' % book
try:
	os.mkdir(dirname)
except OSError as e:
	if e.errno != errno.EEXIST:
		raise

rs = requests.Session()
rs.headers['User-Agent'] = 'Mozilla/5.0'
url = start
i = 0
while url != end:
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
	soup = BeautifulSoup(content, 'lxml')
	next_el = soup.find('a', rel='next')
	if next_el is None:
		url = None
	else:
		url = next_el['href']
	i += 1
