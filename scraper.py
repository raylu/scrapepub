#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup

start = 'https://practicalguidetoevil.wordpress.com/2015/03/25/prologue/'
end = 'https://practicalguidetoevil.wordpress.com/2015/11/04/prologue-2/'

rs = requests.Session()
url = start
i = 0
while url != end:
	name = url.rsplit('/', 2)[1]
	filename = '%02d-%s' % (i, name)
	print 'getting', filename
	content = rs.get(url).content
	with open('raw/' + filename, 'w') as f:
		f.write(content)
	soup = BeautifulSoup(content, 'lxml')
	next_el = soup.find('link', rel='next')
	url = next_el['href']
	i += 1
