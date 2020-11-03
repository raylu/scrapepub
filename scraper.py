#!/usr/bin/env python2

import errno
import os
import os.path
import sys

import requests
from bs4 import BeautifulSoup

bounds = {
	'year1': (
		'https://ceruleanscrawling.wordpress.com/2015/10/03/orientation-1-01/',
		'https://ceruleanscrawling.wordpress.com/2019/09/22/mini-interlude-82-avalons-explanation-heretical-edge/'
	),
	'year2': (
		'https://ceruleanscrawling.wordpress.com/2019/09/23/fusion-1-01-heretical-edge-2/',
		None
	),
}

def main():
	year = sys.argv[1]
	start, end = bounds[year]
	dirname = get_dir(year)

	url = start
	i = 0
	while True:
		content = get_url(dirname, i, url)
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

def get_dir(year):
	dirname = 'hedge_%s_raw/' % year
	try:
		os.mkdir(dirname)
	except OSError as e:
		if e.errno != errno.EEXIST:
			raise
	return dirname

rs = requests.Session()

def get_url(dirname, i, url):
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
	return content

if __name__ == '__main__':
	main()
