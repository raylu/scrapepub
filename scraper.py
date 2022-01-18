#!/usr/bin/env python2

import errno
import os
import os.path
import sys

import requests
from bs4 import BeautifulSoup

bounds = {
	'act1': (
		'https://katalepsis.net/2019/02/02/mind-correlating-1-1/',
		None
	),
}

def main():
	act = sys.argv[1]
	start, end = bounds[act]
	dirname = get_dir(act)

	url = start
	i = 0
	while True:
		content = get_url(dirname, i, url)
		if url == end:
			break
		soup = BeautifulSoup(content, 'lxml')
		next_el = soup.find('a', rel='next')
		if next_el is None:
			if end is None:
				break
			raise Exception('could not find next')
		url = next_el['href']
		i += 1

def get_dir(act):
	dirname = 'katalepsis_%s_raw/' % act
	try:
		os.mkdir(dirname)
	except OSError as e:
		if e.errno != errno.EEXIST:
			raise
	return dirname

rs = requests.Session()
rs.headers['User-Agent'] = 'Mozilla/5.0'

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
