#!/usr/bin/env python

import requests
from xml.etree import ElementTree

rs = requests.Session()
xml = rs.get('http://qntm.org/rss.php?ra').content
rss = ElementTree.fromstring(xml)
urls = []
for item in rss.iter('item'):
	urls.append(item.find('link').text)

for i, url in enumerate(reversed(urls)):
	print 'getting', i, url
	html = rs.get(url).content
	with open('raw/%d' % i, 'w') as f:
		f.write(html)
