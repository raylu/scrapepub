#!/usr/bin/env python

import errno
import os
import os.path
import sys

import requests
from bs4 import BeautifulSoup

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
		'https://tiraas.wordpress.com/2018/04/15/bonus-27-scion-part-4/'
	),
	'vol5': (
		'https://tiraas.wordpress.com/2018/04/16/prologue-volume-5/',
		None
	),
}

bonus_chapters = [
	'https://tiraas.wordpress.com/2015/02/14/bonus-1-captains-orders/',
	'https://tiraas.wordpress.com/2015/02/16/bonus-2-all-those-who-serve/',
	'https://tiraas.wordpress.com/2015/02/18/bonus-3-hero/',
	'https://tiraas.wordpress.com/2015/02/23/bonus-4-heart-of-the-wild/',
	'https://tiraas.wordpress.com/2015/05/08/bonus-5-of-which-reason-knows-nothing/',
	'https://tiraas.wordpress.com/2015/05/11/bonus-6-a-light-in-dark-places/',
	'https://tiraas.wordpress.com/2015/05/13/bonus-7-songbird/',
	'https://tiraas.wordpress.com/2015/05/15/bonus-8-on-being-a-man-part-1/',
	'https://tiraas.wordpress.com/2015/05/18/bonus-9-on-being-a-man-part-2/',
	'https://tiraas.wordpress.com/2015/08/31/bonus-10-along-came-a-spider-part-4/',
	'https://tiraas.wordpress.com/2015/09/04/bonus-11-along-came-a-spider-part-3/',
	'https://tiraas.wordpress.com/2015/09/07/bonus-12-along-came-a-spider-part-2/',
	'https://tiraas.wordpress.com/2015/09/11/bonus-13-along-came-a-spider-part-1/',
	'https://tiraas.wordpress.com/2016/02/27/bonus-14-judgment-and-justice-part-1/',
	'https://tiraas.wordpress.com/2016/07/19/bonus-15-judgment-and-justice-part-2/',
	'https://tiraas.wordpress.com/2016/07/25/bonus-16-justice-and-judgment-part-3/',
	'https://tiraas.wordpress.com/2016/07/27/bonus-17-judgment-and-justice-part-4/',
	'https://tiraas.wordpress.com/2017/07/24/bonus-18-heavy-is-the-head-part-1/',
	'https://tiraas.wordpress.com/2017/07/28/bonus-19-heavy-is-the-head-part-2/',
	'https://tiraas.wordpress.com/2017/07/31/bonus-20-heavy-is-the-head-part-3/',
	'https://tiraas.wordpress.com/2017/08/02/bonus-21-heavy-is-the-head-part-4/',
	'https://tiraas.wordpress.com/2018/04/02/bonus-22-toujours-part-1/',
	'https://tiraas.wordpress.com/2018/04/04/bonus-23-toujours-part-2/',
	'https://tiraas.wordpress.com/2018/04/06/bonus-24-scion-part-1/',
	'https://tiraas.wordpress.com/2018/04/09/bonus-25-scion-part-2/',
	'https://tiraas.wordpress.com/2018/04/15/bonus-26-scion-part-3/',
	'https://tiraas.wordpress.com/2018/04/15/bonus-27-scion-part-4/',
]

def main():
	vol = sys.argv[1]
	if vol == 'bonus':
		scrape_bonus()
		return
	start, end = bounds[vol]
	dirname = get_dir(vol)

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
		if url == 'https://tiraas.wordpress.com/2017/03/24/12-37b/': # skip placeholder chapter
			url = 'https://tiraas.wordpress.com/2017/03/29/12-38/'
		i += 1

def scrape_bonus():
	dirname = get_dir('bonus')

	for i, url in enumerate(bonus_chapters):
		get_url(dirname, i, url)

def get_dir(vol):
	dirname = 'gab_%s_raw/' % vol
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
